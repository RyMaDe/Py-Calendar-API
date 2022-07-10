from django.http import HttpResponse

def index(request):
    return HttpResponse("The PyCalendar Site is up!")