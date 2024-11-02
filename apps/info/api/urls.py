from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfoViewSet

router = DefaultRouter()
router.register(r'', InfoViewSet, basename='info')

urlpatterns = [
    path('', include(router.urls)),
]