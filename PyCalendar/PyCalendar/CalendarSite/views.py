from django.shortcuts import render
from django.views import View

class Index(View):
    def get(self, request):
        print(request.user)
        return render(request, "calendar.html")
