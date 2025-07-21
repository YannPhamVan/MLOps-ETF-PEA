from pathlib import Path

import pandas as pd
from evidently.metric_preset import DataDriftPreset, RegressionPreset, TargetDriftPreset
from evidently.report import Report


def generate_monitoring_reports(reference_path, current_path, output_dir):
    reference_df = pd.read_parquet(reference_path)
    current_df = pd.read_parquet(current_path)

    report = Report(
        metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
            RegressionPreset(),
        ]
    )

    report.run(reference_data=reference_df, current_data=current_df)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "evidently_report.html"
    report.save_html(html_path)
    print(f"Evidently report saved to {html_path}")


if __name__ == "__main__":
    generate_monitoring_reports(
        reference_path="data/df_all.parquet",
        current_path="data/predictions/predictions.parquet",
        output_dir="reports",
    )
