from django.shortcuts import render
# views.py
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class AccountListCreateView(APIView):
    def post(self , request):
        serializer=AccountSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

