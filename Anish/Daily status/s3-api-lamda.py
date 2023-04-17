import json
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = "test-api-lamda-bucket1"
    key = "index.html"
    
    try:
        data = s3.get_object(Bucket=bucket , Key = key)
        json_data = data["Body"].read()
        data = json.load(json_data)
        return {
            "response_code" : 200,
            "data" = data
        }
    except Exception as e:
        print(e)
        raise e
