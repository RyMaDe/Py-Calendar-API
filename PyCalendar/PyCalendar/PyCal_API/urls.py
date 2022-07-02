from django.urls import URLPattern, path, include
from .views import (
    CalendarListAPIView,
    CalendarDetailApiView,
    CalendarSearchAPIView,
)

urlpatterns = [
    path('', CalendarListAPIView.as_view(), name="calendar"),
    path('<int:calendar_id>/', CalendarDetailApiView.as_view(), name = "calendar-item"),
    path('search/', CalendarSearchAPIView.as_view(), name="datesearch"),
]
