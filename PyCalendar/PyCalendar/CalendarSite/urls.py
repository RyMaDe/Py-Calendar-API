from django.urls import path
from .views import Index

app_name = 'CalendarSite'

urlpatterns = [
    path("calendar/", Index.as_view(), name="calendarSite"),
]
