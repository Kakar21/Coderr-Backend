from django.db import models
from django.conf import settings
from django.db.models import Min


class Offer(models.Model):
    """
    Model for offers

    Attributes:
        user (ForeignKey): Reference to the user who created the offer.
        title (CharField): Title of the offer.
        image (ImageField): Optional image associated with the offer.
        description (TextField): Detailed description of the offer.
        created_at (DateTimeField): Timestamp when the offer was created.
        updated_at (DateTimeField): Timestamp when the offer was last updated.
        min_price (DecimalField): Minimum price of the offer details.
        min_delivery_time (PositiveIntegerField): Minimum delivery time in days.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/offers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    min_delivery_time = models.PositiveIntegerField(help_text="Minimum delivery time in days", default=0, editable=False)
    
    def __str__(self):
        return self.title 
    
    def update_min_values(self):
        """
        Updates the minimum price and delivery time for the offer based on its details.
        """
        min_price = self.details.aggregate(Min('price'))['price__min']
        min_delivery_time = self.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        
        self.min_price = min_price or 0 
        self.min_delivery_time = min_delivery_time or 0
        self.save()

class Offerdetail(models.Model):
    """
    Model for offer details, part of an offer

    Attributes:
        offer (ForeignKey): Reference to the associated offer.
        title (CharField): Title of the offer package.
        revisions (IntegerField): Number of revisions allowed.
        delivery_time_in_days (PositiveIntegerField): Delivery time in days.
        price (DecimalField): Price of the package.
        features (JSONField): Features of the package.
        offer_type (CharField): Type of the package (basic, standard, premium).
    """
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
        
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} for {self.offer.title}"