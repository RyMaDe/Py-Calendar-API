from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from PyCalendar.PyCal_API.models import Calendar_API
from django.contrib.auth import get_user_model


class APIListTest(APITestCase):
    calendar_items_url = reverse('calendar')
    token_url = reverse("token_obtain_pair")

    def setUp(self):
        user = get_user_model()
        # Create an initial user to be used, not a superuser.
        self.testuser1 = user.objects.create_user(email="test_user1@user.com", password="password")
        #self.client.login(username="test_user1", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user1@user.com", "password":"password"})
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
        user = get_user_model()
        self.testuser2 = user.objects.create_user(email="test_user2@user.com", password="password")
        #self.client.login(username="test_user2", password="password")  # This is basic authentication
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user2@user.com", "password":"password"})
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
        Author_id = user.objects.get(email="test_user2@user.com").id
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
        user = get_user_model()
        self.testuser1 = user.objects.create_user(email="test_user1@user.com", password="password")
        # self.client.login(username="test_user1", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user1@user.com", "password":"password"})
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

        # Testing the model return statement
        self.assertEqual(str(Calendar_API.objects.first()), "Flight to Paris")

    def test_Get_Permission(self):
        # Testing that a user can only get calendar entries that are posted by them.

        # Creating a new user and making a calendar entry.
        user = get_user_model()
        self.testuser2 = user.objects.create_user(email="test_user2@user.com", password="password")
        #self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user2@user.com", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        data = {
            "Name": "Flight to Rome",
            "Description": "Don't forget passport",
            "Date": "2022-07-05",
            "Time": "13:47:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')
        testuser2_id = user.objects.get(email="test_user2@user.com").id
        testuser1_id = user.objects.get(email="test_user1@user.com").id

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

        # Getting the first id in the user and accessing the url for it.
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

        # Tests that if the calendar entry does not exist, an error is thrown.
        self.calendar_item_url2 = reverse('calendar-item', args = [999999999999])

        response = self.client.put(self.calendar_item_url2, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Testing error is thrown when invalid data is used.
        data = {
            "Name": "Flight to Paris",
            "Description": "Board terminal 6",
            "Date": "2022-105-29",
            "Time": "11:37:00",
            "Tag": "Work",
        }
        response = self.client.put(self.calendar_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Update_Item_Permission(self):
        # Testing that only the creator of a calender entry can edit it.

        # Creating a new user and trying to edit test_user1's calendar entry.
        user = get_user_model()
        self.testuser2 = user.objects.create_user(email="test_user2@user.com", password="password")
        #self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user2@user.com", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Getting the first id in the user and accessing the url for it.
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
        # Getting the first id in the user and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        # Testing that deleting an item removes it fully.
        response = self.client.delete(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing that the item no longer exists after it has been deleted
        response = self.client.get(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Testing that if the calendar entry does not exist, an error is thrown.
        self.calendar_item_url2 = reverse('calendar-item', args = [999999999999])

        response = self.client.delete(self.calendar_item_url2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Delete_Item_Permission(self):
        # Testing that only the creator of a calendar entry can delete that entry.

        # Creating a new user and trying to edit test_user1's calendar entry.
        user = get_user_model()
        self.testuser2 = user.objects.create_user(email="test_user2@user.com", password="password")
        # self.client.login(username="test_user2", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user2@user.com", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Getting the first id in the user and accessing the url for it.
        pk = Calendar_API.objects.first().id
        self.calendar_item_url = reverse('calendar-item', args = [pk])

        # Testing that delete will not work.
        response = self.client.delete(self.calendar_item_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class APISearchTest(APITestCase):
    calendar_items_url = reverse('calendar')
    token_url = reverse("token_obtain_pair")

    def setUp(self):
        user = get_user_model()
        # Create an initial user to be used, not a superuser.
        self.testuser1 = user.objects.create_user(email="test_user1@user.com", password="password")
        #self.client.login(username="test_user1", password="password")
        self.client = APIClient()
        tokens = self.client.post(self.token_url, data={"email":"test_user1@user.com", "password":"password"})
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

        # Making a second post for the user:
        data = {
            "Name": "Flight to Rome",
            "Description": "Bring Camera",
            "Date": "2022-06-20",
            "Time": "13:15:00",
            "Tag": "",
            }
        self.client.post(self.calendar_items_url, data, format='json')

        # Creating a second user and making a post for them too.
        self.testuser2 = user.objects.create_user(email="test_user2@user.com", password="password")
        #self.client.login(username="test_user1", password="password")
        self.client2 = APIClient()
        tokens = self.client2.post(self.token_url, data={"email":"test_user2@user.com", "password":"password"})
        self.client2.credentials(HTTP_AUTHORIZATION="Bearer "+tokens.data["access"])

        # Creating an initial entry for user2.
        data = {
            "Name": "Flight to Berlin",
            "Description": "Board terminal 5",
            "Date": "2022-05-30",
            "Time": "12:00:00",
            "Tag": "",
            }
        self.client2.post(self.calendar_items_url, data, format='json')

    def test_Get_Search(self):
        # Testing that the search will return the correct items by date range,
        # and for the correct user.
        self.search_url = reverse("datesearch")

        # Making the first get request between two dates:
        response = self.client.get(self.search_url, data={"start_date": "2022-05-01",
                    "end_date": "2022-05-31"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that only one item is returned and it belongs to test_user1.
        # The data from testuser2 does not appear.
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["Author"], self.testuser1.id)
        # Making sure the returned data item was in the correct date range.
        self.assertEqual(response.data[0]["Date"], "2022-05-29")

        # Making a request with only a start date:
        response = self.client.get(self.search_url, data={"start_date": "2022-05-01"},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that two items are returned and they belongs to testuser1.
        # The data from testuser2 does not appear.
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["Author"], self.testuser1.id)
        self.assertEqual(response.data[1]["Author"], self.testuser1.id)
        # Making sure the returned data was in the correct date range.
        self.assertEqual(response.data[0]["Date"], "2022-05-29")
        self.assertEqual(response.data[1]["Date"], "2022-06-20")

        # Making a request with only an end date:
        response = self.client.get(self.search_url, data={"end_date": "2022-06-30"},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that two items are returned and they belongs to testuser1.
        # The data from testuser2 does not appear.
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["Author"], self.testuser1.id)
        self.assertEqual(response.data[1]["Author"], self.testuser1.id)
        # Making sure the returned data was in the correct date range.
        self.assertEqual(response.data[0]["Date"], "2022-05-29")
        self.assertEqual(response.data[1]["Date"], "2022-06-20")

        # Making a request without any data:
        response = self.client.get(self.search_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Testing that nothing is returned
        self.assertEqual(response.data, {"res": "No dates entered"})

    def test_Get_Query(self):
        # Testing that search by query will return relevant results.
        self.searchQuery_url = reverse("querysearch")

        # Making the first get request:
        response = self.client.get(self.searchQuery_url, data={"q": "Paris"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that only one item is returned and it belongs to test_user1.
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["Author"], self.testuser1.id)
        # Making sure the returned data item was the correct item.
        self.assertEqual(response.data[0]["Name"], "Flight to Paris")

        # Testing that error is thrown when no query paramenters are given.
        response = self.client.get(self.searchQuery_url, data={"q":""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"res": "No queries entered"})


class APITokenTest(APITestCase):
    token_url = reverse("token_obtain_pair")
    token_refresh_url = reverse("token_refresh")

    def setUp(self):
        user = get_user_model()
        self.testuser1 = user.objects.create_user(email="test_user1@user.com", password="password")
        # self.client.login(username="test_user1", password="password")
        self.client = APIClient()

    def test_get_tokens(self):
        # Testing that the Token authentication system is working and returns
        # the token pair.
        tokens = self.client.post(self.token_url, data={"email":"test_user1@user.com", "password":"password"})
        self.assertEqual(tokens.status_code, status.HTTP_200_OK)
        self.assertIn("access", tokens.data)
        self.assertIn("refresh", tokens.data) 

    def test_refresh_token(self):
        # Testing that the refresh token provided goes through fine and returns
        # an access token.
        tokens = self.client.post(self.token_url, data={"email":"test_user1@user.com", "password":"password"})
        new_access_token = self.client.post(self.token_refresh_url, data={"refresh": tokens.data["refresh"]})
        self.assertEqual(new_access_token.status_code, status.HTTP_200_OK)
        self.assertIn("access", new_access_token.data)

        # Testing that the access token received works by making a simple get request.
        calendar_items_url = reverse('calendar')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+new_access_token.data["access"])
        response = self.client.get(calendar_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
