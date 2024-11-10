from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse


class AuthenticationTests(APITestCase):

    def setUp(self):
        # Set up URLs for registration and login
        self.url = reverse('registration')
        self.url_login = reverse('login')

    def test_users_registration(self):
        # Test user registration with valid data
        data = {
            "username": "test_user",
            "email": "test@beispiel.de",
            "password": "g12345",
            "repeated_password": "g12345",
            "type": "customer"
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check if the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the user is created in the database
        self.assertTrue(User.objects.filter(username=data['username']).exists())

        # Check if a token is created for the user
        user = User.objects.get(username=data['username'])
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_users_login(self):
        # Ensure user registration before login
        self.test_users_registration()
        data = {
            "username": "test_user",
            "password": "g12345"
        }
        response = self.client.post(self.url_login, data, format='json')
        
        # Check if the login response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        

