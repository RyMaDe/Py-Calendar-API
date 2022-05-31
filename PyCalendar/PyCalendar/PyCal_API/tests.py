from django.urls import reverse
from rest_framework.test import APITestCase
from PyCalendar.PyCal_API.views import CalendarListAPIView
from PyCalendar.PyCal_API.views import CalendarDetailApiView
from django.contrib.auth.models import User
from rest_framework import status


class APIListTest(APITestCase):
    calender_items_url = reverse('calendar')

    def setUp(self):
        # Creating an initial entry to be tested.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        self.client.post(self.calender_items_url, data, format='json')

    def test_Entry_Made(self):
        # Testing that posting a new calendar item works.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_Bad_Entry_Data_Name1(self):
        # Testing that posting a new calendar item with invalid data throws an error.
        # Name cannot be empty:
        data = {
            "Name": "",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Bad_Entry_Data_Name2(self):
        # Testing that posting a new calendar item with invalid data throws an error.
        # Name cannot be >50 chars:
        data = {
            "Name": "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Bad_Entry_Data_Date(self):
        # Testing that posting a new calendar item with invalid data throws an error.
        # Date cannot be blank:
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Bad_Entry_Data_Tag(self):
        # Testing that posting a new calendar item with invalid data throws an error.
        # Tag cannot be different to predefined:
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "Hello",
            }
        response = self.client.post(self.calender_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Get_All(self):
        # Testing that all on-going calendar items are returned.
        response = self.client.get(self.calender_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["Name"], "Flight to Paris")


class APIDetailTest(APITestCase):
    calender_items_url = reverse('calendar')
    calendar_item_url = reverse('calendar-item', args = [1])

    def setUp(self):
        # Creating an initial entry to be tested.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        self.client.post(self.calender_items_url, data, format='json')

    def test_Get(self):
        # Testing that getting an item by id returns the correct data.
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Name"], "Flight to Paris")

    def test_Update_Item(self):
        # Testing that changing the data works correctly.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 6",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "Work",
        }
        response = self.client.put(self.calendar_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking that changed fields are changed correctly:
        self.assertEqual(response.data["Description"], "Board terminal 6")
        self.assertEqual(response.data["Tag"], "Work")
        # Checking that unchanged fields remained unchanged:
        self.assertEqual(response.data["Name"], "Flight to Paris")

    def test_Delete_Item(self):
        # Testing that deleting an item removes it fully.
        response = self.client.delete(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing that the item no longer exists after it has been deleted
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
