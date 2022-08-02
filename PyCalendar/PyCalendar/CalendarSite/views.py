from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from PyCalendar.PyCal_API.models import Calendar_API
from .utils import Calendar
from .forms import EventForm
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


class CalendarEvent(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "calendar_event.html"

    def get(self, request, event_id=None):
        try:
            instance = get_object_or_404(Calendar_API, id=event_id)
        except:
            instance = Calendar_API()

        #exists = Calendar_API.objects.filter(id=event_id).exists()
        form = EventForm(instance=instance)
        return render(request, self.template_name, {"form": form})

    def post(self, request, event_id=None):
        try:
            instance = get_object_or_404(Calendar_API, id=event_id)
        except:
            instance = Calendar_API()

        instance.Author = self.request.user
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            item = form.save()
            if item:
                return redirect(reverse("CalendarSite:calendarSite"))
        return render(request, self.template_name, {"form": form})


class CalendarEventDelete(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None

    def get(self, request, event_id):
        item = Calendar_API.objects.filter(Author=request.user, id=event_id)

        if item.exists():
            item.delete()
        return redirect(reverse("CalendarSite:calendarSite"))
