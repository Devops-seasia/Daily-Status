from django.shortcuts import render
from rest_framework.views import APIView
from myapp.models import Accounts
from rest_framework.response import Response
from myapp.serializers import accountSerializers
# Create your views here.

class AccountView(APIView):
    def post(self,request):
        serializer= accountSerializers(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

