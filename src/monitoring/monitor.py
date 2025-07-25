from pathlib import Path
import pandas as pd
import numpy as np
from evidently.metric_preset import DataDriftPreset, RegressionPreset, TargetDriftPreset
from evidently.report import Report
from evidently import ColumnMapping

def generate_monitoring_reports(reference_path, current_path, output_dir):
    reference_df = pd.read_parquet(reference_path)
    current_df = pd.read_parquet(current_path)

    # Check and enforce 'prediction' presence in reference_df
    if 'prediction' not in reference_df.columns:
        reference_df['prediction'] = np.nan

    if 'prediction' not in current_df.columns:
        raise ValueError("'prediction' column missing in current dataset.")
    if 'target' not in reference_df.columns:
        raise ValueError("'target' column missing in reference dataset.")

    # Align features explicitly, excluding 'target' and 'prediction'
    features = [col for col in reference_df.columns if col not in ['target', 'prediction']]

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
