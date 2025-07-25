from pathlib import Path
import pandas as pd
import numpy as np
from evidently.metric_preset import DataDriftPreset, RegressionPreset, TargetDriftPreset
from evidently.report import Report
from evidently import ColumnMapping
import joblib
import src.hotfix_patch_evidently


def generate_monitoring_reports(reference_path, current_path, output_dir):
    reference_df = pd.read_parquet(reference_path)
    current_df = pd.read_parquet(current_path)

    if 'target' not in reference_df.columns:
        raise ValueError("'target' column missing in reference dataset.")
    if 'target' not in current_df.columns:
        raise ValueError("'target' column missing in current dataset.")

    # Charger le modèle pour générer les prédictions sur reference_df
    import mlflow
    from mlflow.exceptions import MlflowException

    model_name = "ETF_PEA_MLOpsZoomcamp"

    try:
        # Essayer de charger la version en Production
        model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
        print("[INFO] Loaded model in Production stage.")
    except MlflowException:
        # Si non disponible, charger la dernière version
        print("[WARN] No model in Production stage. Loading latest version instead.")
        client = mlflow.MlflowClient()
        latest_versions = client.get_latest_versions(model_name, stages=["None"])
        if not latest_versions:
            raise RuntimeError(f"No versions found for model '{model_name}'. Cannot proceed with monitoring.")
        model_uri = f"models:/{model_name}/{latest_versions[0].version}"
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"[INFO] Loaded model version {latest_versions[0].version} for monitoring.")

    reference_df['prediction'] = model.predict(reference_df)
    
    if 'prediction' not in current_df.columns:
        raise ValueError("'prediction' column missing in current dataset.")

    # Exclure Date et ticker si présents
    features = [col for col in reference_df.columns if col not in ['target', 'prediction', 'Date', 'ticker']]

    column_mapping = ColumnMapping(
        target='target',
        prediction='prediction',
        numerical_features=features
    )

    report = Report(
        metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
            RegressionPreset(),
        ]
    )

    report.run(
        reference_data=reference_df,
        current_data=current_df,
        column_mapping=column_mapping
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "evidently_report.html"
    report.save_html(html_path)
    print(f"✅ Evidently report saved to {html_path}")

if __name__ == "__main__":
    generate_monitoring_reports(
        reference_path="data/df_all.parquet",
        current_path="data/predictions/predictions.parquet",
        output_dir="reports",
    )
