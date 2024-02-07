from rest_framework import serializers
from .models import ConfigurationData

class ConfigurationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationData
        fields = '__all__'