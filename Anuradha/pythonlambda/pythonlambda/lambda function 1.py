import boto3
import os
import time
import smtplib
import datetime

ec2 = boto3.client('ec2')

def create_instance():
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
    return response['Instances'][0]['InstanceId']

def get_instance_status(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['State']['Name']

def get_instance_public_ip(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']

def send_email(subject, body):
    from_email = 'anu.rajput4427@gmail.com'
    to_email = 'anu.rajput4427@gmail.com'
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, os.environ['EMAIL_PASSWORD'])
        smtp.sendmail(from_email, to_email, message)

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])

def create_and_install_instance():
    instance_id = None
    instance_status = None
    try:
        instance_id = create_instance()
        print(f"New instance created with ID {instance_id}")
        time.sleep(60) # wait for instance to start
        instance_status = get_instance_status(instance_id)
        print(f"Instance status: {instance_status}")
        if instance_status == 'running':
            public_ip = get_instance_public_ip(instance_id)
            print(f"Instance public IP: {public_ip}")
            send_email("EC2 instance created and nginx installed", f"New EC2 instance created with ID {instance_id} and public IP {public_ip}. Nginx has been installed.")
            stop_instance(instance_id)
            print("EC2 instance has been shut down")
        else:
            send_email("Failed to create EC2 instance", f"Failed to create EC2 instance with ID {instance_id}. Instance status: {instance_status}")
    except Exception as e:
        send_email("Error occurred", str(e))
        if instance_id and instance_status != 'running':
            stop_instance(instance_id)
            print("EC2 instance has been shut down due to error")
