import boto3
from botocore.client import Config


def upload_file_to_s3(local_file_path, bucket_name, s3_key):
    s3_client = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    s3_client.upload_file(local_file_path, bucket_name, s3_key)
    print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
