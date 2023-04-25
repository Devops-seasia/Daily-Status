import boto3
import os

# create a new EC2 client
ec2 = boto3.client('ec2')

# call the describe_instances() method to get information about all instances
response = ec2.describe_instances()

# loop through the reservations and instances to print the instance ID and its status
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']}, Status: {instance['State']['Name']}")

# specify the instance details
instance_type = 't2.micro'
ami_id = 'ami-0aa2b7722dc1b5612'
key_name = 'lambdainstance'
security_group_ids = ['sg-04f480d863b1e3b59']

# launch a new instance
response = ec2.run_instances(
    InstanceType=instance_type,
    ImageId=ami_id,
    KeyName=key_name,
    SecurityGroupIds=security_group_ids,
    MinCount=1,
    MaxCount=1
)

# print the instance ID
instance_id = response['Instances'][0]['InstanceId']
print(f'New instance created with ID: {instance_id}')

