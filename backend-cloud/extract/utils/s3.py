import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_path: str, bucket: str, key: str):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_path, bucket, key)
        print(f"{file_path} uploaded to s3://{bucket}/{key}")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")