from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from PyCalendar.PyCal_API.models import Calendar_API
from django.conf import settings


class APIListTest(APITestCase):
    calendar_items_url = reverse('calendar')
    token_url = reverse("token_obtain_pair")

    def setUp(self):
        # Create an initial user to be used, not a superuser.
        self.testuser1 = settings.AUTH_USER_MODEL.objects.create_user(username="test_user1", password="password")
        #self.client.login(username="test_user1", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user1", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Creating an initial entry to be tested.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')

    def test_Entry_Made(self):
        # Testing that posting a new calendar item works.
        data = {
            "Name": "Flight to Rome",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        response = self.client.post(self.calendar_items_url, data, format='json')
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
        response = self.client.post(self.calendar_items_url, data, format='json')
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
        response = self.client.post(self.calendar_items_url, data, format='json')
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
        response = self.client.post(self.calendar_items_url, data, format='json')
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
        response = self.client.post(self.calendar_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Get_All(self):
        # Testing that all on-going calendar items are returned.
        response = self.client.get(self.calendar_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["Name"], "Flight to Paris")

    def test_Get_All_Permission(self):
        # Creating a second user, posting a calendar entry and making sure only
        # their entry is shown when get request is made and not the first user's.
        self.testuser2 = User.objects.create_user(username="test_user2", password="password")
        #self.client.login(username="test_user2", password="password")  # This is basic authentication
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user2", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        data = {
            "Name": "Flight to Rome",
            "Description": "Don't forget passport",
            "Date": "2022-07-05",
            "Time": "13:47:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')

        response = self.client.get(self.calendar_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that only 1 item is returned, not 2.
        self.assertEqual(len(response.data), 1)
        # Testing the the item that is returned is the above and was posted by the new user.
        Author_id = User.objects.get(username="test_user2").id
        self.assertEqual(response.data[0]["Author"], Author_id)
        self.assertEqual(response.data[0]["Name"], "Flight to Rome")

    def test_Authenticated(self):
        # Testing that the user must be authenticated to access any of the entries.
        Client = APIClient()
        response = Client.get(self.calendar_items_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Testing that the user must be authenticated to access an individual entry.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])
        response = Client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class APIDetailTest(APITestCase):
    calendar_items_url = reverse('calendar')  # URL for all items
    token_url = reverse("token_obtain_pair")

    def setUp(self):
        # Create an initial user to be used, not a superuser.
        self.testuser1 = User.objects.create_user(username="test_user1", password="password")
        # self.client.login(username="test_user1", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user1", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Creating an initial entry to be tested.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 3",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')

    def test_Get(self):
        # Testing that getting an item by id returns the correct data.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Name"], "Flight to Paris")

    def test_Get_Permission(self):
        # Testing that a user can only get calendar entries that are posted by them.

        # Creating a new user and making a calendar entry.
        self.testuser2 = User.objects.create_user(username="test_user2", password="password")
        #self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user2", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        data = {
            "Name": "Flight to Rome",
            "Description": "Don't forget passport",
            "Date": "2022-07-05",
            "Time": "13:47:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')
        testuser2_id = User.objects.get(username="test_user2").id
        testuser1_id = User.objects.get(username="test_user1").id

        # Now checking if the new user can get the above (its own) calendar entry.
        pk = Calendar_API.objects.get(Name="Flight to Rome").id
        self.calendar_item_url = reverse('calendar-item', args = [pk])
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now checking if the new user can get the initial setUp calendar entry.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_Update_Item(self):
        # Testing that changing the data works correctly.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 6",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "Work",
        }

        # Getting the first id in the db and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        response = self.client.put(self.calendar_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking that changed fields are changed correctly:
        self.assertEqual(response.data["Description"], "Board terminal 6")
        self.assertEqual(response.data["Tag"], "Work")
        # Checking that unchanged fields remained unchanged:
        self.assertEqual(response.data["Name"], "Flight to Paris")
        self.assertEqual(response.data["Date"], "2022-05-29")
        self.assertEqual(response.data["Time"], "11:37:00")

    def test_Update_Item_Permission(self):
        # Testing that only the creator of a calender entry can edit it.

        # Creating a new user and trying to edit test_user1's calendar entry.
        self.testuser2 = User.objects.create_user(username="test_user2", password="password")
        #self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user2", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Getting the first id in the db and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 6",
            "Date": "2022-05-29",
            "Time": "11:37:00",
            "Tag": "Work",
        }
        # Testing that the update will not work.
        response = self.client.put(self.calendar_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_Delete_Item(self):
        # Getting the first id in the db and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        # Testing that deleting an item removes it fully.
        response = self.client.delete(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing that the item no longer exists after it has been deleted
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Delete_Item_Permission(self):
        # Testing that only the creator of a calendar entry can delete that entry.

        # Creating a new user and trying to edit test_user1's calendar entry.
        self.testuser2 = User.objects.create_user(username="test_user2", password="password")
        # self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"username":"test_user2", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Getting the first id in the db and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        # Testing that delete will not work.
        response = self.client.delete(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
