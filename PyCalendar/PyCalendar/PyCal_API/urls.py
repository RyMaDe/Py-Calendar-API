from django.urls import URLPattern, path, include
from .views import (
    CalendarListAPIView,
    CalendarDetailApiView,
)

urlpatterns = [
    path('calendar', CalendarListAPIView.as_view()),
    path('calendar/<int:calendar_id>/', CalendarDetailApiView.as_view()),
]
