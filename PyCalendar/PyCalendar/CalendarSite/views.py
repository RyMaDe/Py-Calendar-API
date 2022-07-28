from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from PyCalendar.PyCal_API.models import Calendar_API
from .utils import Calendar
import datetime


class CalendarMain(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "calendar.html"

    def get(self, request):
        items = Calendar_API.objects.filter(Author=request.user)

        today = datetime.date.today()

        # Create the python HTMLCalendar object and adding the user's calendar entries.
        cal = Calendar(today.year, today.month)
        calOut = cal.formatmonth(items, withyear=True)

        return render(request, self.template_name, {"items": items, "calendar": calOut})
