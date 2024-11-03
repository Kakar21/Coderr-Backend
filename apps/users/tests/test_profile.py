from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from apps.users.models import Profile
from django.contrib.auth.models import User


class ProfileTests(APITestCase):
    
    def setUp(self):
        # Create a user and a profile
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        user.save()
        type = 'business'
        self.profile = Profile.objects.create(user=user, type=type)
        
        # Set up the token in the headers for authenticated requests
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_patch_profile(self):
        # URL for the specific profile
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

        # Data for the profile update
        update_data = {
            "first_name": "Test",
            "last_name": "User",
            "location": "Hamburg",
            "tel": "987654321",
            "description": "Updated Description",
            "working_hours": "10-18",
            "email": "testuser123@example.com"
        }

        # Perform the PATCH update
        response = self.client.patch(url, data=update_data, format='json')

        # Check if the PATCH request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the profile was updated correctly
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.location, update_data["location"])
        self.assertEqual(self.profile.tel, update_data["tel"])
        self.assertEqual(self.profile.description, update_data["description"])
        self.assertEqual(self.profile.working_hours, update_data["working_hours"])

        # Ensure that the `type` field was not modified
        self.assertEqual(self.profile.type, "business")

        # Check that the response contains the expected fields
        self.assertIn('user', response.data)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('location', response.data)
        self.assertIn('tel', response.data)
        self.assertIn('description', response.data)
        self.assertIn('working_hours', response.data)
        self.assertIn('type', response.data)
        self.assertIn('created_at', response.data)

        # Verify that the data in the response matches the updated values
        self.assertEqual(response.data['location'], update_data["location"])
        self.assertEqual(response.data['tel'], update_data["tel"])
        self.assertEqual(response.data['description'], update_data["description"])
        self.assertEqual(response.data['working_hours'], update_data["working_hours"])
        self.assertEqual(response.data['email'], update_data["email"])
        self.assertEqual(response.data['first_name'], update_data["first_name"])
        self.assertEqual(response.data['last_name'], update_data["last_name"])
