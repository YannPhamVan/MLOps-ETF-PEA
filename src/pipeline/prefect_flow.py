import json
import subprocess
import sys

from prefect import flow, task

from src.utils.s3_utils import upload_file_to_s3


@task
def ingest_data():
    subprocess.run([sys.executable, "src/data/ingest_etf_data.py"], check=True)

    # Upload to S3 LocalStack
    parquet_files = [
        "data/raw/EWLD_PA.parquet",
        "data/raw/CW8_PA.parquet",
        "data/raw/ESE_PA.parquet",
        "data/raw/PAEEM_PA.parquet",
    ]
    bucket_name = "mlops-etf-pea-bucket"

    for file_path in parquet_files:
        file_name = file_path.split("/")[-1]
        upload_file_to_s3(file_path, bucket_name, f"raw/{file_name}")


@task
def feature_engineering():
    tickers = ["EWLD.PA", "CW8.PA", "ESE.PA", "PAEEM.PA"]
    for ticker in tickers:
        subprocess.run(
            [sys.executable, "src/data/feature_engineering.py", "--ticker", ticker],
            check=True,
        )


@task
def rebuild_dataset():
    subprocess.run([sys.executable, "src/data/rebuild_dataset.py"], check=True)


@task
def train_model():
    subprocess.run(
        [sys.executable, "src/models/train_model.py", "--tracking_uri", "mlruns"],
        check=True,
    )


@task
def predict():
    subprocess.run([sys.executable, "src/models/predict.py"], check=True)


@task
def display_metrics():
    with open("data/metrics/metrics.json", "r") as f:
        metrics = json.load(f)
    print(
        f"Model Evaluation Metrics:\n"
        f"RMSE: {metrics['RMSE']:.5f}\n"
        f"R2: {metrics['R2']:.5f}"
    )


@task
def run_monitoring():
    # subprocess.run([sys.executable, "src/monitoring/monitor.py"], check=True)
    pass


@flow
def etf_pipeline_flow():
    ingest_data()
    feature_engineering()
    rebuild_dataset()
    train_model()
    predict()
    display_metrics()
    run_monitoring()


if __name__ == "__main__":
    etf_pipeline_flow()
