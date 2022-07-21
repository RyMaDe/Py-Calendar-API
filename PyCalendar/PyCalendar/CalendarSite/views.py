from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from PyCalendar.PyCal_API.models import Calendar_API


class Index(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None

    def get(self, request):
        print(request.user)
        items = Calendar_API.objects.filter(Author=request.user)
        return render(request, "calendar.html", {"items": items})
