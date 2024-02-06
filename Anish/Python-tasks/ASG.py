import boto3
# Create an Auto Scaling client
autoscaling_client = boto3.client('autoscaling')
# Define the launch configuration
launch_config_name = "my-launch-config1"
image_id = 'ami-00952f27cf14db9cd'
instance_type = 't2.micro'

response = autoscaling_client.create_launch_configuration(
    LaunchConfigurationName=launch_config_name,
    ImageId=image_id,
    InstanceType=instance_type
)


# Define the Auto Scaling Group
asg_name = 'my-asg'
min_size = 2
max_size = 5
desired_capacity = 3
availability_zones = ['ap-south-1a', 'ap-south-1b']

response = autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    LaunchConfigurationName=launch_config_name,
    MinSize=min_size,
    MaxSize=max_size,
    DesiredCapacity=desired_capacity,
    AvailabilityZones=availability_zones
)

#List Auto Scaling Groups (ASGs)
response = autoscaling_client.describe_auto_scaling_groups()

for asg in response['AutoScalingGroups']:
    print(f"Auto Scaling Group: {asg['AutoScalingGroupName']}")
    print(f"Launch Configuration: {asg['LaunchConfigurationName']}")
    print(f"Min Size: {asg['MinSize']}")
    print(f"Max Size: {asg['MaxSize']}")
    print(f"Desired Capacity: {asg['DesiredCapacity']}")
    print()

#delete the ASG group
response = autoscaling_client.delete_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    ForceDelete=True 
)

#delete the launch configuration
response = autoscaling_client.delete_launch_configuration(
    LaunchConfigurationName=launch_config_name
)
