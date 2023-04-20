import boto3
import os


ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')


AMI_ID = 'ami-069aabeee6f53e7bf'
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'mykey'
SECURITY_GROUP_IDS = ['sg-050e5e9bae758b8bd']
USER_DATA = '''
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install nginx -y
'''

def lambda_handler(event, context):
    instance_id = None
    try:
        instance_id = os.environ['INSTANCE_ID']
    except KeyError:
        pass
    
    if instance_id:
        
        response = ec2.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        
        if state != 'running':
            instance_id = None
    
    if not instance_id:
        
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SecurityGroupIds=SECURITY_GROUP_IDS,
            UserData=USER_DATA,
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
    
    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    

    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ['sudo yum install -y nginx', 'sudo systemctl start nginx']}
    )
    
    return {
        'statusCode': 200,
        'body': f'Instance {instance_id} is running and software has been installed'
    }
