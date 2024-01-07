from django.urls import path
from .views import *

urlpatterns = [
    path('', Home , name="home"),
    path('login/' ,Login, name="login"),
    path('register/' ,register, name="register"),
    path('logout/' ,Logout, name="logout"),
    path('activate/<uidb64>/<token>/',activate, name='activate'), 
    path('make-an-appointment/', Appointments , name="appointment"),
    path('manage-appointment/', ManageAppointments , name="manage"),
    path('filter-appointment/', FilterAppointments , name="filter"),
    path('my-appointment/', UserAppointment , name="myappointment"),
]
