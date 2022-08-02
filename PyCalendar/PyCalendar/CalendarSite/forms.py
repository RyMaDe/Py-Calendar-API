from django.forms import ModelForm
from PyCalendar.PyCal_API.models import Calendar_API

class EventForm(ModelForm):
    class Meta:
        model = Calendar_API
        fields = fields = ["id", "Name", "Description", "Date", "Time", "Tag"]
