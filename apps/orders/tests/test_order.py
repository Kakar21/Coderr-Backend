from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.orders.models import Order
from apps.offers.models import Offer, Offerdetail

class OrderTests(APITestCase):
    """
    Test cases for the Order API
    """
    def setUp(self):
        # Create users and profiles for different roles
        self.customer_user = User.objects.create_user(username="customer", password="testpass")
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        
        self.business_user = User.objects.create_user(username="business", password="testpass")
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        
        self.staff_user = User.objects.create_user(username="staff", password="testpass", is_staff=True)
        self.staff_profile = Profile.objects.create(user=self.staff_user)

        # Generate authentication tokens for each user
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.staff_token = Token.objects.create(user=self.staff_user)

        # Create a test offer and offer details
        self.offer = Offer.objects.create(user=self.business_user, title="Logo Design")
        self.offer_detail = Offerdetail.objects.create(
            offer=self.offer, title="Basic Design", revisions=3, delivery_time_in_days=5, 
            price=150.00, features=["Logo Design", "Business Cards"], offer_type="basic"
        )

        self.order_url = reverse('order-list')
        self.order_detail_url = lambda pk: reverse('order-detail', kwargs={'pk': pk})

    def test_create_order_as_customer(self):
        # Test if a customer can successfully create an order
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.post(self.order_url, {"offer_detail_id": self.offer_detail.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_as_non_customer(self):
        # Test that a business user cannot create an order
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.post(self.order_url, {"offer_detail_id": self.offer_detail.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_orders(self):
        # Test if a customer can retrieve their orders
        Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order_status_as_customer(self):
        # Test if a customer can update the status of an order
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.patch(self.order_detail_url(order.id), {"status": "completed"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "completed")

    def test_update_order_with_invalid_field(self):
        # Test that a customer cannot update a non-allowed field
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.patch(self.order_detail_url(order.id), {"price": 200.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order_as_staff(self):
        # Test if a staff member can delete an order
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.delete(self.order_detail_url(order.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_delete_order_as_non_staff(self):
        # Test that a regular user cannot delete an order
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.delete(self.order_detail_url(order.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
