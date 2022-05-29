from django.urls import reverse
from rest_framework.test import APITestCase
from PyCalendar.PyCal_API.views import CalendarListAPIView
from django.contrib.auth.models import User
from rest_framework import status


class APIViewTest(APITestCase):
    calender_items_url = reverse('calendar')

    def setUp(self):
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        self.client.post(self.calender_items_url, data, format='json')

    def test_Entry_Made(self):
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
