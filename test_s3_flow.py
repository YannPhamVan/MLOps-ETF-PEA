from prefect import flow, task
import boto3
import os

AWS_ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "test-bucket"
FILE_KEY = "test_file.txt"
CONTENT = "Hello from Prefect + LocalStack!"

@task
def write_test_file_to_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        endpoint_url=AWS_ENDPOINT_URL,
    )
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass

    s3.put_object(Bucket=BUCKET_NAME, Key=FILE_KEY, Body=CONTENT.encode("utf-8"))
    print(f"✅ Uploaded {FILE_KEY} to {BUCKET_NAME}")

@task
def read_test_file_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        endpoint_url=AWS_ENDPOINT_URL,
    )
    response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    data = response["Body"].read().decode("utf-8")
    print(f"✅ Retrieved content: {data}")

@flow
def test_s3_flow():
    write_test_file_to_s3()
    read_test_file_from_s3()

if __name__ == "__main__":
    test_s3_flow()
