from django.urls import path, include
from .views import BaseInfoView

urlpatterns = [
    path('', BaseInfoView.as_view(), name='base-info'),
]