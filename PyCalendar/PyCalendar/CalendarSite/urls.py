from django.urls import path
from . import views

app_name = 'CalendarSite'

urlpatterns = [
    path("calendar/", views.index, name="calendar"),
]
