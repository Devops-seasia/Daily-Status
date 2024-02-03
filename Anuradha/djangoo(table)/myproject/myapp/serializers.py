from rest_framework import serializers
from myapp.models import CloudAccount 

class CloudAccountSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = CloudAccount
        fields = '__all__'
