from rest_framework import generics
from .models import ConfigurationData
from .serializers import ConfigurationDataSerializer

class ConfigurationDataCreateAPIView(generics.CreateAPIView):
    queryset = ConfigurationData.objects.all()
    serializer_class = ConfigurationDataSerializer
