import json
import boto3

ec2 = boto3.resource('ec2')
id = 'instance_id'

instance_id = id
    
instance = ec2.Instance(instance_id)
response = instance.terminate()
    
print(f"Terminating instance {instance_id}")
    
"return"
{
    'statusCode': 200,
    'body': f"Instance {instance_id} terminated successfully"
    }
