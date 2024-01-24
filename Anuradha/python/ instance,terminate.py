import boto3

def create_instance(image_id, instance_type, min_count, max_count, key_name, instance_name):
    ec2 = boto3.resource("ec2")

    # Create an EC2 instance
    instances = ec2.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=min_count,
        MaxCount=max_count,
        KeyName=key_name,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': instance_name}
                ]
            }
        ]
    )

    # Assuming you're creating only one instance
    instance = instances[0]
    print(f"Instance {instance.id} with Name '{instance_name}' created successfully.")

    return instance

def list_instances():
    ec2 = boto3.resource("ec2")

    # Get all instances
    instances = ec2.instances.all()

    print("Listing all instances:")
    for instance in instances:
        print(f"Instance ID: {instance.id}, Instance Type: {instance.instance_type}, Launch Time: {instance.launch_time}")

def main():
    try:
        # Prompt user for instance details
        image_id = input("Enter your image-id: ")
        instance_type = input("Enter your instancetype: ")
        min_count = int(input("Enter the Mincount: "))
        max_count = int(input("Enter the Maxcount: "))
        key_name = "anuec2"
        
        # Prompt user for instance name
        instance_name = input("Enter a name for your instance: ")

        # Create an EC2 instance
        instance = create_instance(image_id, instance_type, min_count, max_count, key_name, instance_name)

        # List all instances
        list_instances()

        # Prompt user to terminate the instance
        terminate = input("Do you want to terminate the instance? (yes/no): ")
        
        if terminate.lower() == 'yes':
            # Terminate the instance
            instance.terminate()
            print(f"Instance {instance.id} terminated successfully.")

    except KeyboardInterrupt:
        print("\nOperation aborted by user.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
