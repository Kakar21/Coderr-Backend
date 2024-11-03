from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=254, unique=True)
    # first_name = models.CharField(max_length=254)
    # last_name = models.CharField(max_length=254)
    file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=254)
    tel = models.CharField(max_length=254)
    description = models.TextField()
    working_hours = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=[('business', 'Business'), ('customer', 'Customer')])
    # email = models.EmailField(max_length=254, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

