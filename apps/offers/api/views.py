from rest_framework import generics 
from .serializers import OfferSerializer, OfferDetailSerializer, OfferdetailsSerializer
from apps.offers.models import Offer, Offerdetail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import OfferPagination
from .filters import OfferFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsBusinessOrReadOnly


class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination
    permission_classes = [IsBusinessOrReadOnly]


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['get', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({}, status=status.HTTP_200_OK)


class OfferdetailsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offerdetail.objects.all()
    serializer_class = OfferdetailsSerializer
    permission_classes = [IsBusinessOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.offer.update_min_values()
