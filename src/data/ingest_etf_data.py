import os
from pathlib import Path

import boto3
import yfinance as yf


def download_etf_data(etf_list, start_date, end_date, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for etf in etf_list:
        try:
            data = yf.download(etf, start=start_date, end=end_date, interval="1d")
            data.to_parquet(f"{output_dir}/{etf.replace('.', '_')}.parquet")
            print(f"{etf} downloaded: {data.shape[0]} rows.")
        except Exception as e:
            print(f"Error downloading {etf}: {e}")


if __name__ == "__main__":
    etf_list = ["EWLD.PA", "PAEEM.PA", "ESE.PA", "CW8.PA"]  # Modifiable
    start_date = "2020-07-01"
    end_date = "2025-07-01"
    output_dir = "../data/raw"

    download_etf_data(etf_list, start_date, end_date, output_dir)


def upload_to_localstack(local_file, bucket, s3_key):
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )
    s3.upload_file(str(local_file), bucket, s3_key)
    print(f"Uploaded {local_file} to s3://{bucket}/{s3_key}")


if __name__ == "__main__":
    # ingestion code...

    raw_data_folder = Path("data/raw")
    bucket_name = "mlops-etf-pea-bucket"

    for parquet_file in raw_data_folder.glob("*.parquet"):
        s3_key = f"ingested/{parquet_file.name}"
        upload_to_localstack(parquet_file, bucket_name, s3_key)
