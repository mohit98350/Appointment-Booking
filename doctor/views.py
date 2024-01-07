from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_str,force_bytes
from django.contrib.auth import authenticate, login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect ,HttpResponse
from django.contrib import messages
from .models import Appointment
import datetime
from django.template.loader import get_template,render_to_string
from twilio.rest import Client 
from .token import account_activation_token
from .pagination import Pagination

def Home(request):
    if request.method == 'POST':
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")

        email=EmailMessage(
            subject=f"{name} from doctor family",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]

        )

        email.send()
        return HttpResponse("Email sent succesfully..")

    
    return render(request , 'index.html')

def register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
     
        if len(username) > 20:
            return redirect("/")

        if pass1!=pass2:
            return redirect("/")

        myuser=User.objects.create_user(username,email,pass1)
        myuser.is_active = False
        myuser.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('account_activate.html', {
                'user': myuser,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': account_activation_token.make_token(myuser),
            })
      
        email=EmailMessage(
           mail_subject,
           message,
            to=[email]

        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
       
    else:
        return render(request , "register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request,messages.SUCCESS,f"Thank you for your email confirmation. Now you can login to your account")
        return redirect("login")
    else:
        return HttpResponse('Activation link is invalid!')


def Login(request):
       
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username , password = password)
        if user is not None:
            login(request , user)
            return redirect("appointment")
        else:
          
            messages.add_message(request , messages.WARNING,f"Oops !! You have entered wrong credientials")
            return HttpResponseRedirect(request.path)

    return render(request ,'login.html')

def Logout(request):
    logout(request)
    return redirect("/")


def Appointments(request):
    if not request.user.is_authenticated:
     return render(request , 'register.html')
    print(request.user)
   
    if request.method == 'POST':
        fname=request.POST.get("fname")  
        lname=request.POST.get("lname")  
        email=request.POST.get("email")  
        mobile=request.POST.get("mobile")  
        message=request.POST.get("request")  

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message


        )
        appointment.user_appointment=request.user
        appointment.save()

        messages.add_message(request , messages.SUCCESS,f"Thanks {message} for making an appointment,we will email you in ASAP!!")
        return HttpResponseRedirect(request.path)

    
    return render(request , 'appointment.html')


def FilterAppointments(request):
    filterappointments=Appointment.objects.all()
   

    if request.method == 'GET':
        st=request.GET.get('sort')
        if st!=None:
            if st=='Accepted':

                filterappointments=Appointment.objects.filter(accepted=True)

            elif st == 'Pending':
                  filterappointments=Appointment.objects.filter(accepted=False)  
            else:
                filterappointments=Appointment.objects.all() 
      
        appointments= Pagination(request,filterappointments)
        context={
        "appointments":appointments,
        "st":st
    }

    return render(request , 'manage-appointments.html',context)




@login_required
def ManageAppointments(request):
    appointments=Appointment.objects.all()
    appointments= Pagination(request,appointments)
  
    if request.method == 'POST':
        date=request.POST.get("date")
        time=request.POST.get("time")
        appointment_id=request.POST.get("appointment-id")
        appointment=Appointment.objects.get(id=appointment_id)
        appointment.accepted=True
        appointment.accepted_date=datetime.datetime.now()
        appointment.time=time
        appointment.save()

        data={
            "fname":appointment.first_name,
            "date":date,
            "time":time
        }

        message = get_template('email.html').render(data)

        # SENDING EMAIL

        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()
      
    #   SENDING SMS

        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages \
        .create(
         body=f'Appointment Confiramtion with Family Doctor X is set to {date} and time slot is {time}. ',
         from_=settings.TWILIO_PHONE_NUMBER,
         to= str("+") + str(91) + str(appointment.phone))

        messages.add_message(request,messages.SUCCESS,f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path) 
    context={
        "appointments":appointments,
        "title":"Manage appointments"
    }
     
    return render(request , 'manage-appointments.html',context)
    
@login_required
def UserAppointment(request):
    user = request.user
    appointments=Appointment.objects.filter(user_appointment=user).filter(accepted=True)
    appointments= Pagination(request,appointments)
    context={
        "appointments":appointments,
        "title":"My appointment"
    }    
    
    return render(request,'manage-appointments.html',context)    