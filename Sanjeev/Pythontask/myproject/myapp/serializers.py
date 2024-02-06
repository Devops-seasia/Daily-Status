from rest_framework import serializers
from myapp.models import Accounts

class accountSerializers(serializers.ModelSerializer):
    class Meta:
        model= Accounts
        fields='__all__'
