import boto3

# Create an ELBv2 client
elbv2_client = boto3.client('elbv2')

# Define the target group name and protocol
target_group_name = 'my-target-group'
protocol = 'HTTP'

response = elbv2_client.create_target_group(
    Name=target_group_name,
    Protocol=protocol,
    Port=80, 
    VpcId='vpc-06a74ede0057b4562' 
)

target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
print(f'Target Group ARN: {target_group_arn}')


#List Target Groups
response = elbv2_client.describe_target_groups()

for target_group in response['TargetGroups']:
    print(f"Target Group ARN: {target_group['TargetGroupArn']}")
    print(f"Target Group Name: {target_group['TargetGroupName']}")
    print(f"Protocol: {target_group['Protocol']}")
    print(f"Port: {target_group['Port']}")
    print()

elbv2_client.delete_target_group(
    TargetGroupArn=target_group_arn
)
