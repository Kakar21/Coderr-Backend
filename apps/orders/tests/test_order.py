from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.orders.models import Order
from apps.offers.models import Offer, Offerdetail

class OrderTests(APITestCase):
    def setUp(self):
        # Kundenbenutzer und zugehöriges Profil erstellen
        self.customer_user = User.objects.create_user(username="customer", password="testpass")
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        
        # Business-Benutzer und zugehöriges Profil erstellen
        self.business_user = User.objects.create_user(username="business", password="testpass")
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        
        # Staff-Benutzer erstellen
        self.staff_user = User.objects.create_user(username="staff", password="testpass", is_staff=True)
        self.staff_profile = Profile.objects.create(user=self.staff_user)

        # Tokens generieren
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.staff_token = Token.objects.create(user=self.staff_user)

        # Testangebot und -details erstellen
        self.offer = Offer.objects.create(user=self.business_user, title="Logo Design")
        self.offer_detail = Offerdetail.objects.create(
            offer=self.offer, title="Basic Design", revisions=3, delivery_time_in_days=5, 
            price=150.00, features=["Logo Design", "Visitenkarten"], offer_type="basic"
        )

        self.order_url = reverse('order-list')
        self.order_detail_url = lambda pk: reverse('order-detail', kwargs={'pk': pk})

    def test_create_order_as_customer(self):
        # Setzt das Token des Kunden für die Anfrage
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        # Bestellung erstellen
        response = self.client.post(self.order_url, {"offer_detail_id": self.offer_detail.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_as_non_customer(self):
        # Setzt das Token des Business-Benutzers (kein Kunde) für die Anfrage
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)

        # Bestellung erstellen
        response = self.client.post(self.order_url, {"offer_detail_id": self.offer_detail.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Keine Berechtigung für Business-Benutzer

    def test_list_orders(self):
        # Erstellt eine Bestellung als Kunde
        Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        # Bestellungen abrufen
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order_status_as_customer(self):
        # Erstellt eine Bestellung
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        # Bestellung mit neuem Status aktualisieren
        response = self.client.patch(self.order_detail_url(order.id), {"status": "completed"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "completed")

    def test_update_order_with_invalid_field(self):
        # Erstellt eine Bestellung
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        # Versucht, ein nicht zulässiges Feld zu aktualisieren
        response = self.client.patch(self.order_detail_url(order.id), {"price": 200.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Nicht zulässig, nur `status` ist erlaubt

    def test_delete_order_as_staff(self):
        # Bestellung erstellen
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)

        # Bestellung löschen
        response = self.client.delete(self.order_detail_url(order.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})  # Leere JSON-Antwort
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_delete_order_as_non_staff(self):
        # Bestellung erstellen
        order = Order.objects.create(customer_user=self.customer_user, offer_detail=self.offer_detail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        # Versuch der Bestellungslöschung durch einen normalen Benutzer (kein Staff)
        response = self.client.delete(self.order_detail_url(order.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Keine Berechtigung für Nicht-Staff-Benutzer
