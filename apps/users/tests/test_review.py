from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.users.models import Review
from django.contrib.auth.models import User


class ReviewViewTests(APITestCase):
    
    def setUp(self):
        # Create a business user and a reviewer user
        self.business_user = User.objects.create_user(username='businessuser', password='password123')
        self.reviewer_user = User.objects.create_user(username='revieweruser', password='password123')

        # URL for the Review API
        self.url = reverse('review-list')  # Adjust the name if using a URL name convention

    def test_create_review(self):
        """
        Tests creating a new review through the API.
        """
        self.client.force_authenticate(user=self.reviewer_user)
        data = {
            "business_user": self.business_user.id,
            "reviewer": self.reviewer_user.id,
            "rating": 5,
            "description": "Great service!"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['description'], "Great service!")
        self.assertEqual(response.data['business_user'], self.business_user.id)

    def test_get_reviews(self):
        """
        Tests retrieving all reviews for a business user.
        """
        # Create some reviews in the database
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.reviewer_user,
            rating=4,
            description="Good service."
        )
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.reviewer_user,
            rating=3,
            description="Average experience."
        )

        # Authenticate and make the GET request
        self.client.force_authenticate(user=self.reviewer_user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['rating'], 4)
        self.assertEqual(response.data[1]['rating'], 3)
