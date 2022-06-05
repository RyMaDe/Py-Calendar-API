from django.urls import URLPattern, path, include
from .views import (
    CalendarListAPIView,
    CalendarDetailApiView,
)

urlpatterns = [
    path('calendar', CalendarListAPIView.as_view(), name = "calendar"),
    path('calendar/<int:calendar_id>/', CalendarDetailApiView.as_view(), name = "calendar-item"),
]
