from rest_framework import serializers
from .models import Calendar_API


class Calendar_API_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar_API
        fields = ["id", "Name", "Description", "Date", "Time", "Tag", "Author"]
