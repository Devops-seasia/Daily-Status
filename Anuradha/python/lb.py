import boto3

def create_load_balancer(lb_name, subnet_ids, security_group_id):
    elbv2 = boto3.client('elbv2')

    if len(subnet_ids) < 2:
        print("Error: At least two subnets in different Availability Zones are required.")
        return None

    # Create an Application Load Balancer
    elb_response = elbv2.create_load_balancer(
        Name=lb_name,
        Subnets=subnet_ids,
        SecurityGroups=[security_group_id],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': lb_name
            },
        ]
    )

    print(f"Load Balancer {elb_response['LoadBalancers'][0]['LoadBalancerName']} created successfully.")

    return elb_response['LoadBalancers'][0]['LoadBalancerArn']

def list_load_balancers():
    elbv2 = boto3.client('elbv2')

    # Get all Application Load Balancers
    load_balancers = elbv2.describe_load_balancers()

    print("Listing all Load Balancers:")
    for lb in load_balancers['LoadBalancers']:
        print(f"Load Balancer Name: {lb['LoadBalancerName']}")

def delete_load_balancer(load_balancer_arn):
    elbv2 = boto3.client('elbv2')

    # Delete the Application Load Balancer
    elbv2.delete_load_balancer(
        LoadBalancerArn=load_balancer_arn
    )

    print(f"Load Balancer with ARN {load_balancer_arn} deleted successfully.")

def main():
    try:
        # Prompt user for Load Balancer details
        lb_name = input("Enter Load Balancer Name: ")
        subnet_ids = input("Enter comma-separated Subnet IDs (at least two in different AZs): ").split(',')
        security_group_id = input("Enter Security Group ID: ")

        # Create a Load Balancer
        load_balancer_arn = create_load_balancer(lb_name, subnet_ids, security_group_id)

        if load_balancer_arn:
            # List all Load Balancers
            list_load_balancers()

            # Prompt user to delete the Load Balancer
            delete_lb = input("Do you want to delete the Load Balancer? (yes/no): ")

            if delete_lb.lower() == 'yes':
                # Delete the Load Balancer
                delete_load_balancer(load_balancer_arn)

    except KeyboardInterrupt:
        print("\nOperation aborted by user.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
