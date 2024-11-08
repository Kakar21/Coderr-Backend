from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomerOrReadOnly


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer_user=user) | Order.objects.filter(offer_detail__offer__user=user)

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)
