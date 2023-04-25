import boto3
import json
import os
import time
import smtplib
import datetime

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

# specify userdata script to install nginx
userdata = """#!/bin/bash
sudo apt-get update
sudo apt-get install -y nginx
sudo systemctl start nginx
"""

# launch a new instance
response = ec2.run_instances(
    InstanceType=instance_type,
    ImageId=ami_id,
    KeyName=key_name,
    UserData=userdata,
    SecurityGroupIds=security_group_ids,
    MinCount=1,
    MaxCount=1
    
)

# print the instance ID
instance_id = response['Instances'][0]['InstanceId']
print(f'New instance created with ID: {instance_id}')




#-----------------------------------------------------------IP Address------------------------------------------------------------------




# get the public IP address of the instance
response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print(f"New instance created with ID {instance_id} and public IP {public_ip}")

print(public_ip)





#-------------------------------------------------------Email-------------------------------------------------



# Define the instance ID of the instance you want to shut down
instance_id = 'YOUR_INSTANCE_ID'

# Define the email address you want to send the email to
to_email = 'anu.rajput4427@gmail.com'

def second_function():
    # Do something in the second function
    FunctionName='my-second-function', 
    print("Second function executed successfully")

def first_function():
    # Call the second function
    second_function()

    # Shut down the instance
    ec2.stop_instances(InstanceIds=[instance_id])

    # Send an email
    from_email = 'anu.rajput4427@gmail.com'
    subject = 'EC2 instance shutdown'
    body = 'The EC2 instance has been shut down.'
    message = f"Subject: {subject}\n\n{body}"
    
    # Create an SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, 'YOUR_EMAIL_PASSWORD')
        smtp.sendmail(from_email, to_email, message)
    
    print("Email sent successfully")
    
# Schedule the first function to run every day at 11 am IST
while True:
    now = datetime.datetime.now()
    if now.hour == 11 and now.minute == 0 and now.second == 0:
        first_function()
        break
    time.sleep(1)


