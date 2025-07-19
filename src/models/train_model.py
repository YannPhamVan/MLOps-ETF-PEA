#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
from pathlib import Path

import mlflow
import pandas as pd
from lightgbm import LGBMRegressor
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def train_model(data_path: Path, tracking_uri: str, experiment_name: str) -> None:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    df = pd.read_parquet(data_path)
    logging.info("Data shape: %s", df.shape)

    feature_cols = [col for col in df.columns if col not in ["target", "ticker"]]
    # Exclude 'Date' and other non-numeric columns if present
    feature_cols = [
        col
        for col in feature_cols
        if col != "Date" and pd.api.types.is_numeric_dtype(df[col])
    ]

    X = df[feature_cols]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    client = MlflowClient()
    try:
        client.create_registered_model(experiment_name)
        logging.info("Registered model '%s' created.", experiment_name)
    except MlflowException as e:
        if "already exists" in str(e):
            logging.info(
                "Registered model '%s' already exists, continuing.", experiment_name
            )
        else:
            raise e

    params = {
        "learning_rate": 0.01,
        "num_leaves": 31,
        "max_depth": -1,
        "random_state": 42,
    }

    with mlflow.start_run() as run:
        print(f"Run ID: {run.info.run_id}")
        mlflow.log_params(params)

        model = LGBMRegressor(**params, n_estimators=100)

        model.fit(
            X_train,
            y_train,
            eval_set=[(X_test, y_test)],
            callbacks=None,
        )

        y_pred = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        logging.info("Training completed with RMSE: %.5f, R2: %.5f", rmse, r2)

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=experiment_name,
            input_example=X_test.iloc[:5],
        )
        logging.info("Model logged and registered under '%s'", experiment_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train ETF PEA model with LightGBM and MLflow"
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default=str(Path(__file__).resolve().parents[2] / "data" / "df_all.parquet"),
        help="Path to input data parquet file",
    )
    parser.add_argument(
        "--tracking_uri",
        type=str,
        default="file:///G:/Mon Drive/DataTalksClub/MLOps-ETF-PEA/mlruns",
        help="MLflow tracking URI",
    )
    parser.add_argument(
        "--experiment_name",
        type=str,
        default="ETF_PEA_MLOpsZoomcamp",
        help="MLflow experiment name",
    )

    args = parser.parse_args()

    train_model(
        data_path=Path(args.data_path),
        tracking_uri=args.tracking_uri,
        experiment_name=args.experiment_name,
    )
