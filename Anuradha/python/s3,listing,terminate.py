import boto3

def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3')

    # Create an S3 bucket
    s3.create_bucket(Bucket=bucket_name)

    print(f"S3 Bucket {bucket_name} created successfully.")

    return bucket_name

def configure_static_website(bucket_name):
    s3 = boto3.client('s3')

    # Configure the S3 bucket as a static website
    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}
        }
    )

    print(f"S3 Bucket {bucket_name} configured as a static website.")

def list_s3_buckets():
    s3 = boto3.client('s3')

    # Get all S3 buckets
    buckets = s3.list_buckets()

    print("Listing all S3 Buckets:")
    for bucket in buckets['Buckets']:
        print(f"S3 Bucket Name: {bucket['Name']}")

def delete_s3_bucket(bucket_name):
    s3 = boto3.client('s3')

    # Delete the S3 bucket
    s3.delete_bucket(Bucket=bucket_name)

    print(f"S3 Bucket {bucket_name} deleted successfully.")

def main():
    try:
        # Prompt user for S3 bucket name
        bucket_name = input("Enter S3 Bucket Name: ")

        # Create an S3 bucket
        create_s3_bucket(bucket_name)

        # Configure S3 bucket as a static website
        configure_static_website(bucket_name)

        # List all S3 buckets
        list_s3_buckets()

        # Prompt user to delete the S3 bucket
        delete_s3 = input("Do you want to delete the S3 Bucket? (yes/no): ")

        if delete_s3.lower() == 'yes':
            # Delete the S3 bucket
            delete_s3_bucket(bucket_name)

    except KeyboardInterrupt:
        print("\nOperation aborted by user.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
