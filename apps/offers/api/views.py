from rest_framework import generics 
from .serializers import OfferSerializer, OfferdetailsSerializer
from apps.offers.models import Offer, Offerdetail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import OfferPagination
from .filters import OfferFilter
from rest_framework import filters


class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination


class OfferdetailsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offerdetail.objects.all()
    serializer_class = OfferdetailsSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.offer.update_min_values()
