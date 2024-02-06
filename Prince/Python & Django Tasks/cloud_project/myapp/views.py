from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ConfigurationData
from .serializers import ConfigurationDataSerializer

class CreateConfigAPIView(APIView):
    def post(self, request):
        serializer = ConfigurationDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
