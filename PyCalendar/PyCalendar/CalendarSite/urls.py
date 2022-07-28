from django.urls import path
from .views import CalendarMain

app_name = 'CalendarSite'

urlpatterns = [
    path("calendar/", CalendarMain.as_view(), name="calendarSite"),
]
