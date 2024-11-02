from rest_framework import viewsets 
from .serializers import InfoSerializer
from apps.info.models import Info

class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

