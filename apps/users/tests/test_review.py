from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.users.models import Review, Profile
from django.contrib.auth.models import User


class ReviewListTests(APITestCase):
    
    def setUp(self):
        # Create a business user and a reviewer user
        self.business_user = User.objects.create_user(username='businessuser', password='password123')
        self.reviewer_user = User.objects.create_user(username='revieweruser', password='password123')

        # Create profiles for each user with appropriate types
        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.reviewer_user, type='customer')

        # URL for the Review API
        self.url = reverse('review-list')  # Adjust the name if using a URL name convention

    def test_create_review(self):
        """
        Tests that only customer users can create a review for a business,
        and only one review per customer-business pair is allowed.
        """
        # Authenticate as customer user
        self.client.force_authenticate(user=self.reviewer_user)
        # Data for the review
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Great service!"
        }
        
        # First attempt to create a review (should succeed)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['description'], "Great service!")
        self.assertEqual(response.data['business_user'], self.business_user.id)
        self.assertEqual(response.data['reviewer'], self.reviewer_user.id)  # Check that reviewer is set automatically

        # Second attempt to create a review for the same business by the same customer (should fail)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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


class ReviewDetailTests(APITestCase):
    
    def setUp(self):
        # Create a business user and two reviewer users
        self.business_user = User.objects.create_user(username='businessuser', password='password123')
        self.reviewer_user = User.objects.create_user(username='revieweruser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        # Create profiles with appropriate types
        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.reviewer_user, type='customer')
        Profile.objects.create(user=self.other_user, type='customer')

        # Create a review by the reviewer_user
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.reviewer_user,
            rating=5,
            description="Great service!"
        )

        # URL for the specific review
        self.url = reverse('review-detail', kwargs={'pk': self.review.id})

    def test_retrieve_review(self):
        """Test that any authenticated user can retrieve the review."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 5)

    def test_update_and_delete_review_as_reviewer(self):
        """Test that the reviewer can update and delete their own review."""
        self.client.force_authenticate(user=self.reviewer_user)
        
        # Test updating the review
        update_data = {"rating": 4, "description": "Updated service!"}
        response = self.client.patch(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)

        # Test deleting the review
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_update_and_delete_review_as_other_user(self):
        """Test that a different user cannot update or delete the review."""
        self.client.force_authenticate(user=self.other_user)
        
        # Test that update fails
        response = self.client.patch(self.url, {"rating": 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test that delete fails
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())