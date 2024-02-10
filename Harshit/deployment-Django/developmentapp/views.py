from rest_framework import generics
from .models import ConfigurationData
from .serializers import ConfigurationDataSerializer
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse

import json



class ConfigurationDataCreateAPIView(generics.CreateAPIView):
    queryset = ConfigurationData.objects.all() #queryset: This attribute specifies the queryset that will be used to retrieve objects for this view. In this case, ConfigurationData.objects.all()
    serializer_class = ConfigurationDataSerializer


def get_all_data(request):
    # Retrieve all data for YourModel1
    model1_data = ConfigurationData.objects.all()

  

    # Serialize the data for both models
    model1_json_data = serialize('json', model1_data)
   

    # You can add more models if needed

    # Combine the JSON data into a single dictionary
    all_data = {
        'model1_data': json.loads(model1_json_data),
       
        # Add more model data here if needed
    }

    # Return the combined JSON data as a response
    return JsonResponse(all_data)