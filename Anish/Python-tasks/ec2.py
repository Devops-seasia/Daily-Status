import boto3
ec2_client = boto3.client('ec2')

# Specify the parameters for the new instance
instance_params = {
    'ImageId' : 'ami-0d980397a6e8935cd',
    'InstanceType' : 't2.micro',
    'MinCount' : 1,
    'MaxCount' : 1,
    'KeyName' : 'Ani-key',
    'UserData': '''#!/bin/bash
                    echo "Hello, World!" > index.html
                    nohup python -m SimpleHTTPServer 80 &'''

}

# Launch the EC2 instance
response = ec2_client.run_instances(**instance_params)

instance_id = response['Instances'][0]['InstanceId']

print(f"Instance {instance_id} is being created.")

# Step 2: List all instances with their type and launch time

response = ec2_client.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        launch_time = instance['LaunchTime']

        print(f"Instance ID : {instance_id}, instance Type : {instance_type}, Launch Time : {launch_time}")

# Step 3: Terminate the created instance
ec2_client.terminate_instances(InstanceIds=[instance_id])
print(f"Instance {instance_id} terminated.")
