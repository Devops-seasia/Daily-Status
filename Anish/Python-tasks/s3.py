import boto3

# Create an S3 client
s3_client = boto3.client('s3')

# Define the bucket name
bucket_name = 'my-test-bucket342'  
# Create S3 bucket
s3_client.create_bucket(
    Bucket=bucket_name,
)

# Enable static website hosting
s3_client.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'error.html'}
    }
)

#listing s3 buckets
response = s3_client.list_buckets()

for bucket in response['Buckets']:
    print(f"S3 Bucket Name: {bucket['Name']}")
    print(f"Creation Date: {bucket['CreationDate']}")
    print()

# Delete the S3 bucket
s3_client.delete_bucket(
    Bucket=bucket_name
)
