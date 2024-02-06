import boto3
# Create an ELB client
elbv2_client = boto3.client('elbv2')

# Create a load balancer
response = elbv2_client.create_load_balancer(
    Name='MyLoadBalancer',
    Subnets = ['subnet-06cbc63adb91f007b','subnet-0b6c96049fd7ed4af'],
    SecurityGroups = ['sg-026f4267f9b6b069d'],
    Scheme = 'internet-facing',
    Tags =[
        {
            'Key' : 'Name',
            'Value' : 'MyLoadBalancer'

        },
    ]
)

load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
print(f"Load Balancer created with ARN: {load_balancer_arn}")

# List load balancers
response = elbv2_client.describe_load_balancers()

print("List of Load Balancers:")
for lb in response['LoadBalancers']:
    print(f"Load Balancer Name: {lb['LoadBalancerName']}, ARN: {lb['LoadBalancerArn']}")

# Delete the load balancer
elbv2_client.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
print(f"Load Balancer with ARN {load_balancer_arn} deleted.")
