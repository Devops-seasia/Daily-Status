import boto3
import os
import time


def create_ec2_instance():
    ec2 = boto3.client('ec2')
    ami_id = 'ami-02396cdd13e9a1257'
    instance_type = 't2.micro'
    key_name = 'tas1'
    security_group_ids = ['sg-06261257280012655']
    user_data = '''
        #!/bin/bash
        sudo yum update -y
        sudo amazon-linux-extras install nginx -y
    '''
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        UserData=user_data,
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    return instance_id


def check_instance_status(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    return state


def wait_until_instance_running(instance_id):
    ec2 = boto3.client('ec2')
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])


def install_nginx_and_stop_instance(instance_id):
    ssm = boto3.client('ssm')
    email_subject = 'automated mail'
    email_body = 'check the mail'
    recipient_email = 'princhauhan10@gmail.com'
    sender_email = 'princechauhan0961@gmail.com'

    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ['sudo yum install -y nginx', 'sudo systemctl start nginx']}
    )

    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=[instance_id])

    ses = boto3.client('ses')
    ses.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': email_subject},
            'Body': {'Text': {'Data': email_body}}
        }
    )


def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    if instance_id and check_instance_status(instance_id) == 'running':
        wait_until_instance_running(instance_id)
    else:
        instance_id = create_ec2_instance()
        wait_until_instance_running(instance_id)
    install_nginx_and_stop_instance(instance_id)
    return {
        'statusCode': 200,
        'body': 'Instance has been stopped and email has been sent'
    }
