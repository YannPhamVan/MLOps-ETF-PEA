#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import logging
from pathlib import Path

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.metrics import r2_score, root_mean_squared_error

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def predict_returns(
    experiment_name: str,
    tracking_uri: str,
    data_path: Path,
    predictions_dir: Path,
) -> None:
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    # Load latest model version
    latest_versions = client.get_latest_versions(experiment_name, stages=["None"])
    model_uri = f"models:/{experiment_name}/{latest_versions[0].version}"
    model = mlflow.pyfunc.load_model(model_uri)
    logging.info(
        "Loaded model version %s from MLflow registry", latest_versions[0].version
    )

    # Load data
    df_all = pd.read_parquet(data_path)
    logging.info("Data shape: %s", df_all.shape)

    feature_cols = [col for col in df_all.columns if col not in ["target", "ticker"]]
    X = df_all[feature_cols]
    y_true = df_all["target"]

    # Predict
    y_pred = model.predict(X)
    df_all["prediction"] = y_pred

    # Save predictions
    predictions_dir.mkdir(parents=True, exist_ok=True)
    pred_file = predictions_dir / "predictions.parquet"
    df_all.to_parquet(pred_file, index=False)
    logging.info("Predictions saved to %s", pred_file)

    # Evaluation
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    logging.info("Evaluation -> RMSE: %.5f, R2: %.5f", rmse, r2)
    metrics = {"RMSE": rmse, "R2": r2}

    # Récupérer l'experiment_id par nom
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found.")
    experiment_id = experiment.experiment_id

    # Log metrics dans une run liée à l'experience correcte
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_metrics(metrics)

    # Sauvegarde locale pour Prefect
    metrics_path = Path("data/metrics")
    metrics_path.mkdir(parents=True, exist_ok=True)
    with open(metrics_path / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Predict ETF forward returns with registered MLflow model."
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default=None,
        help="Path to parquet dataset",
    )
    parser.add_argument(
        "--predictions_dir",
        type=str,
        default=None,
        help="Directory to save predictions",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    experiment_name = "ETF_PEA_MLOpsZoomcamp"
    tracking_uri = f"file:///{project_root}/mlruns"

    data_path = (
        Path(args.data_path)
        if args.data_path
        else project_root / "data" / "df_all.parquet"
    )
    predictions_dir = (
        Path(args.predictions_dir)
        if args.predictions_dir
        else project_root / "data" / "predictions"
    )

    predict_returns(experiment_name, tracking_uri, data_path, predictions_dir)
