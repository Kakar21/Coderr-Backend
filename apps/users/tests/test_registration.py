from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('registration')

    def test_user_registration(self):
        data = {
            "username": "test_user",
            "email": "test@beispiel.de",
            "password": "g12345",
            "repeated_password": "g12345",
            "type": "customer"
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(User.objects.filter(username=data['username']).exists())

        user = User.objects.get(username=data['username'])
        self.assertTrue(Token.objects.filter(user=user).exists())
