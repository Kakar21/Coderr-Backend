from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    file = models.ImageField(upload_to='images/profiles/', null=True, blank=True)
    location = models.CharField(max_length=254)
    tel = models.CharField(max_length=254)
    description = models.TextField()
    working_hours = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=[('business', 'Business'), ('customer', 'Customer')])
    # email = models.EmailField(max_length=254, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="received_reviews"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="given_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.business_user} - Rating: {self.rating}"


