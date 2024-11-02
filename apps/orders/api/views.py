from rest_framework import viewsets 
from .serializers import OrdersSerializer
from apps.orders.models import Orders

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

