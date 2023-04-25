import boto3
import os
import time
import datetime
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Check if instance is running or not
    response = ec2.describe_instances()
    running_instance_id = 'InstanceId'
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                running_instance_id = instance['InstanceId']
                break
    
    # If instance is not running, create a new instance
    if not running_instance_id:
        instance_type = 't2.micro'
        ami_id = 'ami-0aa2b7722dc1b5612'
        key_name = 'lambdainstance'
        security_group_ids = ['sg-04f480d863b1e3b59']
        
        userdata = """#!/bin/bash
        sudo apt-get update
        sudo apt-get install -y nginx
        sudo systemctl start nginx
        """
        
        response = ec2.run_instances(
            InstanceType=instance_type,
            ImageId=ami_id,
            KeyName=key_name,
            UserData=userdata,
            SecurityGroupIds=security_group_ids,
            MinCount=1,
            MaxCount=1
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f'New instance created with ID: {instance_id}')
        
        # Call Lambda function 2 to shut down the instance and send an email
        lambda_client = boto3.client('lambda')
        payload = {
            'instance_id': instance_id
        }
        response = lambda_client.invoke(
            FunctionName='Lambda-Function-2',
            Payload=json.dumps(payload)
        )
        print(response)
    else:
        print(f'Instance {running_instance_id} is already running')
