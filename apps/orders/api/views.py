from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomerForPost, IsStaffOrReadOnlyForDestroy
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from apps.users.models import Profile

class OrderViewSet(viewsets.ModelViewSet):
    """
    This ViewSet class provides CRUD functionalities for orders.
    - Authenticated users can view their own orders.
    - Staff members can view all orders.
    - Only the status of an order can be updated.
    - Orders can be deleted by staff users.
    """
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


class OrderCountView(APIView):
    """
    Returns the number of ongoing orders for a specific business user.
    """
    def get(self, request, business_user_id):
        try:
            business_user = Profile.objects.get(id=business_user_id)
        except Profile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if business_user.type != 'business':
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            order_count = Order.objects.filter(
                offer_detail__offer__user=business_user.user,
                status='in_progress'
            ).count()
        
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    Returns the number of completed orders for a specific business user.
    """
    def get(self, request, business_user_id):
        try:
            business_user = Profile.objects.get(id=business_user_id)
        except Profile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if business_user.type != 'business':
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            completed_order_count = Order.objects.filter(
                offer_detail__offer__user=business_user.user,
            status='completed'
        ).count()
        
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)
