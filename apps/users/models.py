from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
    

class Profile(models.Model):
    """
    Profile model extending the Django User model with additional attributes.

    Properties:
        user: Associated Django User.
        first_name: User's first name.
        last_name: User's last name.
        file: Optional profile image.
        location: User's location.
        tel: User's telephone number.
        description: User's bio or description.
        working_hours: User's working hours.
        type: User type, either 'business' or 'customer'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    file = models.ImageField(upload_to='images/profiles/', null=True, blank=True)
    location = models.CharField(max_length=254)
    tel = models.CharField(max_length=254)
    description = models.TextField()
    working_hours = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=[('business', 'Business'), ('customer', 'Customer')])

    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    """
    Review model for storing user reviews.

    Properties:
        business_user: User receiving the review.
        reviewer: User giving the review.
        rating: Rating given by the reviewer.
        description: Text of the review.
        created_at: When the review was created.
        updated_at: When the review was last updated.
    """
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


