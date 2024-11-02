from rest_framework import serializers 
from apps.offers.models import Offers

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'