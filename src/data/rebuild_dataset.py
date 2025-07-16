#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def rebuild_dataset(features_dir: Path, output_file: Path) -> None:
    dfs = []

    for file in features_dir.glob("*.parquet"):
        df = pd.read_parquet(file)

        # Clean multi-index columns if needed
        new_cols = []
        for col in df.columns:
            if isinstance(col, str):
                col_clean = (
                    col.replace("('", "")
                    .replace("', '')", "")
                    .replace("', '", "_")
                    .replace("')", "")
                )
            else:
                col_clean = (
                    "_".join([c for c in col if c]) if isinstance(col, tuple) else col
                )
            new_cols.append(col_clean)
        df.columns = new_cols

        # Add ticker column
        ticker = file.stem.replace("_features", "")
        df["ticker"] = ticker

        dfs.append(df)

    # Concatenate all DataFrames
    df_all = pd.concat(dfs, ignore_index=True)

    # Check that target exists
    if "target" not in df_all.columns:
        logging.error("Target column missing.")
    else:
        logging.info("Target column present.")
        missing = df_all["target"].isna().sum()
        logging.info(f"Missing values in target: {missing}")

    # Save dataset for training
    df_all.to_parquet(output_file, index=False)
    logging.info(f"Dataset saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--features_dir", type=str, default=None, help="Path to features directory"
    )
    parser.add_argument(
        "--output_file", type=str, default=None, help="Output parquet file path"
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    features_dir = (
        Path(args.features_dir)
        if args.features_dir
        else project_root / "data" / "features"
    )
    output_file = (
        Path(args.output_file)
        if args.output_file
        else project_root / "data" / "df_all.parquet"
    )

    rebuild_dataset(features_dir, output_file)
