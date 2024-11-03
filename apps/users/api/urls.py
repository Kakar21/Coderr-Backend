from django.urls import path, include
from .views import ProfileDetail, ProfileList

urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('business/', ProfileList.as_view(), {'type': 'business'}, name='profile-business'),
    path('customer/', ProfileList.as_view(), {'type': 'customer'}, name='profile-customer'),
]
