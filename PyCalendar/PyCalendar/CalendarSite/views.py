from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from PyCalendar.PyCal_API.models import Calendar_API
from .utils import Calendar
import datetime
import calendar


class CalendarMain(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "calendar.html"

    def get(self, request):
        items = Calendar_API.objects.filter(Author=request.user)

        qdate = self.request.GET.get("date", None)
        today = get_date(qdate)
        nextMonth = next_month(today)
        prevMonth = prev_month(today)

        # Create the python HTMLCalendar object and adding the
        # user's calendar entries.
        cal = Calendar(today.year, today.month)
        calOut = cal.formatmonth(items, withyear=True)

        context = {"items": items, "calendar": calOut,
            "next_month": nextMonth, "prev_month":prevMonth}

        return render(request, self.template_name, context)

def get_date(day):
    if day:
        year, month = map(int, day.split("-"))
        return datetime.date(year, month, day=1)
    return datetime.date.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'date=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'date=' + str(next_month.year) + '-' + str(next_month.month)
    return month
