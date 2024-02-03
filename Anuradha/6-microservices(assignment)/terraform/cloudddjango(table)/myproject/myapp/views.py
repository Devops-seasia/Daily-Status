from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from myapp.serializers import CloudAccountSerializer
from myapp.services import CloudAccountService
from myapp.models import CloudAccount
from rest_framework.permissions import IsAuthenticated
from myapp import serializers

class CloudAccountView(APIView):
    

    def post(self, request, format=None):
        serializer = CloudAccountSerializer(data=request.data)
        if serializer.is_valid():
            cloud_account_service = CloudAccountService()

            # Extract other fields from the serializer
            other_fields = {field: serializer.validated_data.get(field) for field in ['account_type', 'account_id', 'secret_key', 'region', 'app_id', 'client_id', 'secret_id', 'tenant_id']}

            access_key = serializer.validated_data.get('access_key')
            
            # Combine other fields with the encoded access_key
            response_data = {'access_key': access_key, **other_fields}

            # Save the details in the database
            cloud_account = CloudAccount(**response_data)
            cloud_account.save()

            return Response(response_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        This method is used to retrieve all cloud accounts with decrypted access key.
        """
        cloud_accounts = CloudAccount.objects.filter(is_active=True).order_by("id")
        serializer = CloudAccountSerializer(cloud_accounts, many=True)

        # Modify the serialized data to include the decrypted access key
        data = []
        for item in serializer.data:
            access_key = item.get('access_key')
            item['access_key'] = access_key  # Replace encrypted access key with decrypted one
            data.append(item)

        result = {
            'data': data,
            'code': HTTP_200_OK,
            'message': 'OK',
        }
        return Response(result, status=HTTP_200_OK)