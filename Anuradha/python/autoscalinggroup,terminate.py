import boto3

def create_launch_configuration(image_id, instance_type, key_name, launch_config_name):
    autoscaling = boto3.client('autoscaling')

    # Create a Launch Configuration
    autoscaling.create_launch_configuration(
        LaunchConfigurationName=launch_config_name,
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
    )

    print(f"Launch Configuration {launch_config_name} created successfully.")

def create_auto_scaling_group(launch_config_name):
    autoscaling = boto3.client('autoscaling')

    # Prompt user for Auto Scaling Group details
    asg_name = input("Enter Auto Scaling Group Name: ")
    min_size = int(input("Enter the minimum size: "))
    max_size = int(input("Enter the maximum size: "))
    desired_capacity = int(input("Enter the desired capacity: "))
    subnet_ids = input("Enter comma-separated Subnet IDs: ").split(',')

    # Create an Auto Scaling Group
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName=launch_config_name,
        MinSize=min_size,
        MaxSize=max_size,
        DesiredCapacity=desired_capacity,
        VPCZoneIdentifier=','.join(subnet_ids),
        Tags=[
            {
                'Key': 'Name',
                'Value': asg_name,
                'PropagateAtLaunch': True
            },
        ]
    )

    print(f"Auto Scaling Group {asg_name} created successfully.")

def terminate_auto_scaling_group(asg_name):
    autoscaling = boto3.client('autoscaling')

    # Terminate the Auto Scaling Group
    autoscaling.delete_auto_scaling_group(AutoScalingGroupName=asg_name, ForceDelete=True)

    print(f"Auto Scaling Group {asg_name} terminated successfully.")

def main():
    try:
        # Prompt user for Launch Configuration details
        image_id = input("Enter EC2 image ID: ")
        instance_type = input("Enter EC2 instance type: ")
        key_name = input("Enter EC2 key name: ")
        launch_config_name = input("Enter Launch Configuration Name: ")

        # Create a Launch Configuration
        create_launch_configuration(image_id, instance_type, key_name, launch_config_name)

        # Create an Auto Scaling Group
        create_auto_scaling_group(launch_config_name)

        # Prompt user to terminate the Auto Scaling Group
        terminate_asg = input("Do you want to terminate the Auto Scaling Group? (yes/no): ")

        if terminate_asg.lower() == 'yes':
            # Terminate the Auto Scaling Group
            asg_name = input("Enter the name of the Auto Scaling Group to terminate: ")
            terminate_auto_scaling_group(asg_name)

    except KeyboardInterrupt:
        print("\nOperation aborted by user.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
