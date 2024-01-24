import boto3

def create_target_group():
    elbv2 = boto3.client('elbv2')

    # Prompt user for Target Group details
    tg_name = input("Enter Target Group Name: ")
    protocol = input("Enter protocol (HTTP/HTTPS): ")
    port = int(input("Enter port: "))
    vpc_id = input("Enter VPC ID: ")

    # Create a Target Group
    tg_response = elbv2.create_target_group(
        Name=tg_name,
        Protocol=protocol,
        Port=port,
        VpcId=vpc_id,
        HealthCheckProtocol='HTTP',
        HealthCheckPort='traffic-port',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2,
        Matcher={
            'HttpCode': '200'
        }
    )

    print(f"Target Group {tg_response['TargetGroups'][0]['TargetGroupName']} created successfully.")

    return tg_response['TargetGroups'][0]['TargetGroupArn']

def list_target_groups():
    elbv2 = boto3.client('elbv2')

    # Get all Target Groups
    target_groups = elbv2.describe_target_groups()

    print("Listing all Target Groups:")
    for tg in target_groups['TargetGroups']:
        print(f"Target Group ARN: {tg['TargetGroupArn']}, Target Group Name: {tg['TargetGroupName']}")

def delete_target_group(target_group_arn):
    elbv2 = boto3.client('elbv2')

    # Delete the Target Group
    elbv2.delete_target_group(TargetGroupArn=target_group_arn)

    print(f"Target Group {target_group_arn} deleted successfully.")

def main():
    try:
        # Create a Target Group
        target_group_arn = create_target_group()

        # List all Target Groups
        list_target_groups()

        # Prompt user to delete the Target Group
        delete_tg = input("Do you want to delete the Target Group? (yes/no): ")

        if delete_tg.lower() == 'yes':
            # Delete the Target Group
            delete_target_group(target_group_arn)

    except KeyboardInterrupt:
        print("\nOperation aborted by user.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
