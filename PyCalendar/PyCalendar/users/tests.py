from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'testuser@super.com')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', password='password')

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'testuser@user.com')

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', password='password')

    def test_new_user_Post(self):
        # Testing that the url post request works with valid data.
        url = reverse("users:Create_user")

        data = {"email": "testuser@a.com", "first_name": "test" ,"password": "password"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {"email": "", "password": "password"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
