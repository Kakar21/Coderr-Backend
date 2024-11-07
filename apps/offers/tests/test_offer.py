from rest_framework.test import APITestCase
from django.urls import reverse
from apps.offers.models import Offer, Offerdetail
from apps.users.models import Profile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class OfferCreateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offer-list')

    def test_create_offer_with_details(self):
        data = {
            "title": "Test Offer",
            "description": "A test description for the offer",
            "details": [
                {
                    "title": "Basic Plan",
                    "revisions": 1,
                    "delivery_time_in_days": 5,
                    "price": "100.00",
                    "features": {"feature1": "Basic feature"},
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Plan",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": "200.00",
                    "features": {"feature1": "Standard feature"},
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Plan",
                    "revisions": 3,
                    "delivery_time_in_days": 1,
                    "price": "300.00",
                    "features": {"feature1": "Premium feature"},
                    "offer_type": "premium"
                }
            ]
        }

        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        offer = Offer.objects.get(title="Test Offer")
        self.assertEqual(offer.user, self.user)
        self.assertEqual(offer.title, "Test Offer")
        self.assertEqual(offer.description, "A test description for the offer")
        
        self.assertEqual(offer.min_price, 100.00)
        self.assertEqual(offer.min_delivery_time, 1)
        
        details = Offerdetail.objects.filter(offer=offer)
        self.assertEqual(details.count(), 3)
        
        offer_types = set(detail.offer_type for detail in details)
        self.assertEqual(offer_types, {'basic', 'standard', 'premium'})
