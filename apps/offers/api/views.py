from rest_framework import viewsets 
from .serializers import OffersSerializer
from apps.offers.models import Offers

class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer
    
