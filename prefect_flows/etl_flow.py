from prefect import flow, task
from subprocess import run
from pathlib import Path

@task
def feature_engineering_task(ticker="EWLD.PA"):
    cmd = f"python src/data/feature_engineering.py --ticker {ticker}"
    result = run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError("Feature engineering failed")

@task
def rebuild_dataset_task():
    cmd = "python src/data/rebuild_dataset.py"
    result = run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError("Rebuild dataset failed")

@task
def train_model_task():
    cmd = "python src/models/train_model.py"
    result = run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError("Train model failed")

@task
def predict_task():
    cmd = "python src/models/predict.py"
    result = run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError("Predict failed")

@flow
def etf_pipeline(ticker="EWLD.PA"):
    feature_engineering_task(ticker)
    rebuild_dataset_task()
    train_model_task()
    predict_task()

if __name__ == "__main__":
    etf_pipeline()
