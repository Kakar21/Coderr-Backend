from django.db import models
from apps.offers.models import Offerdetail
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders')
    offer_detail = models.ForeignKey(Offerdetail, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def business_user(self):
        return self.offer_detail.offer.user  

    @property
    def title(self):
        return self.offer_detail.offer.title  

    @property
    def revisions(self):
        return self.offer_detail.revisions  

    @property
    def delivery_time_in_days(self):
        return self.offer_detail.delivery_time_in_days  

    @property
    def price(self):
        return self.offer_detail.price  

    @property
    def features(self):
        return self.offer_detail.features  

    @property
    def offer_type(self):
        return self.offer_detail.offer_type 

    def __str__(self):
        return f"Order {self.id} - {self.title} - {self.status}"