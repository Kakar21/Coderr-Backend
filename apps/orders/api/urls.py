from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
]