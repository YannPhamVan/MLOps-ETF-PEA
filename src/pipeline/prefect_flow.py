import subprocess

from prefect import flow, task


@task
def ingest_data():
    subprocess.run(["python", "src/data/ingest_etf_data.py"], check=True)


@task
def feature_engineering():
    subprocess.run(
        ["python", "src/data/feature_engineering.py", "--ticker", "EWLD.PA"], check=True
    )
    subprocess.run(
        ["python", "src/data/feature_engineering.py", "--ticker", "CW8.PA"], check=True
    )
    subprocess.run(
        ["python", "src/data/feature_engineering.py", "--ticker", "ESE.PA"], check=True
    )
    subprocess.run(
        ["python", "src/data/feature_engineering.py", "--ticker", "PAEEM.PA"],
        check=True,
    )


@task
def rebuild_dataset():
    subprocess.run(["python", "src/data/rebuild_dataset.py"], check=True)


@task
def train_model():
    subprocess.run(["pipenv", "run", "python", "src/models/train_model.py"], check=True)


@task
def predict():
    subprocess.run(["python", "src/models/predict.py"], check=True)


@flow
def etf_pipeline_flow():
    ingest_data()
    feature_engineering()
    rebuild_dataset()
    train_model()
    predict()


if __name__ == "__main__":
    etf_pipeline_flow()
