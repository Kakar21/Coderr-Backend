from django.urls import path
from .views import OfferListView, OfferDetailView

urlpatterns = [
    path('', OfferListView.as_view(), name='offer-list'),
    path('<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
]
