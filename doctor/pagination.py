from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def Pagination(request,appointments):
    page = request.GET.get('page', 1)

    paginator = Paginator(appointments, 3)
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    return appointments