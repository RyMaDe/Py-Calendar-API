from django.urls import path
from .views import CalendarMain, CalendarEvent, CalendarEventDelete

app_name = 'CalendarSite'

urlpatterns = [
    path("calendar/", CalendarMain.as_view(), name="calendarSite"),
    path("calendar/edit/<int:event_id>/", CalendarEvent.as_view(), name="calendarEdit"),
    path("calendar/new/", CalendarEvent.as_view(), name="calendarNew"),
    path("calendar/delete/<int:event_id>/", CalendarEventDelete.as_view(), name="calendarDelete"),
]
