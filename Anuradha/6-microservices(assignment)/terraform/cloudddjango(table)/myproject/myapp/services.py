from myapp.models import CloudAccount , EC2Instance
from rest_framework.exceptions import ValidationError
# Import the datetime module
from datetime import datetime, timedelta

import boto3
from django.conf import settings



class CloudAccountService:
    def save_cloud_account(self, data):
        try:
            account_type = data.get('account_type')
            account_id = data.get('account_id')
            access_key = data.get('access_key', '')
            secret_key = data.get('secret_key', '')
            region = data.get('region', '')
            app_id = data.get('app_id', '')
            client_id = data.get('client_id', '')
            secret_id = data.get('secret_id', '')
            tenant_id = data.get('tenant_id', '')

            cloud_account = CloudAccount(
                account_type=account_type,
                account_id=account_id,
                access_key=access_key,
                secret_key=secret_key,
                region=region,
                app_id=app_id,
                client_id=client_id,
                secret_id=secret_id,
                tenant_id=tenant_id,
            )

            cloud_account.save()

            return cloud_account

        except Exception as e:
            raise ValidationError({'error': str(e)})
        



    def get_aws_ec2_instances(self, access_key, secret_key, region):
        try:
            # Create an AWS EC2 client
            ec2_client = boto3.client(
                'ec2',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )

            # Retrieve the list of EC2 instances
            response = ec2_client.describe_instances()

            # Extract relevant information from the response and store in the database
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # Extract information such as instance_id, instance_type, etc.
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']

                    # Store the information in the database (adjust the fields accordingly)
                    ec2_instance = EC2Instance(
                        instance_id=instance_id,
                        instance_type=instance_type,
                        # ... (add more fields as needed)
                    )
                    ec2_instance.save()

        except Exception as e:
            print(f"Error fetching or storing EC2 instances: {e}")
            raise ValidationError({'error': str(e)})

    