from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomerForPost, IsStaffOrReadOnlyForDestroy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnlyForDestroy, IsCustomerForPost]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer_user=user) | Order.objects.filter(offer_detail__offer__user=user)

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)

    def update(self, request, *args, **kwargs):

        if list(request.data.keys()) != ["status"] or request.data["status"] not in dict(Order.STATUS_CHOICES):
            return Response(
                {"detail": "Only the 'status' field can be updated with a valid choice."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = self.get_object()
        instance.status = request.data['status']
        instance.save(update_fields=['status'])
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({}, status=status.HTTP_200_OK)
