from rest_framework import serializers
from .models import ConfigurationData

class ConfigurationDataSerializer(serializers.ModelSerializer):#his line defines a serializer class named ConfigurationDataSerializer that inherits from serializers.ModelSerializer. ModelSerializer is a subclass of Serializer that automatically generates serializer fields based on the model fields.
    class Meta:#This inner class Meta provides metadata for the serializer. Here:
        model = ConfigurationData# specifies the model that this serializer is associated with, in this case, the ConfigurationData model.
        fields = '__all__'