#!/usr/bin/env python
# coding: utf-8

import argparse
from pathlib import Path

import pandas as pd


def compute_features(df, window_fwd=30):
    """Calcule les features et la target pour le modèle."""
    df = df.copy()
    df["daily_return"] = df["Close"].pct_change()
    df["weekly_return"] = df["Close"].pct_change(5)
    df["monthly_return"] = df["Close"].pct_change(21)
    df["rolling_volatility_21"] = df["daily_return"].rolling(21).std()
    df["rolling_volatility_63"] = df["daily_return"].rolling(63).std()
    df["momentum_21"] = df["Close"] / df["Close"].shift(21) - 1
    df["momentum_63"] = df["Close"] / df["Close"].shift(63) - 1
    df["ma_21"] = df["Close"].rolling(21).mean()
    df["ma_63"] = df["Close"].rolling(63).mean()
    df["drawdown"] = (df["Close"] / df["Close"].cummax()) - 1
    df["target"] = df["Close"].pct_change(window_fwd).shift(-window_fwd)
    df = df.dropna()
    return df


def main(ticker: str, window_fwd: int = 30):
    # Déterminer le dossier projet
    project_dir = Path(__file__).resolve().parents[2]
    raw_dir = project_dir / "data" / "raw"
    features_dir = project_dir / "data" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)

    # Charger les données
    file_name = f"{ticker.replace('.', '_')}.parquet"
    df = pd.read_parquet(raw_dir / file_name).reset_index().sort_values("Date")

    # Calculer les features
    df_features = compute_features(df, window_fwd=window_fwd)

    # Sauvegarder
    output_file = features_dir / f"{ticker.replace('.', '_')}_features.parquet"
    df_features.to_parquet(output_file, index=False)
    print(f"[OK] Features saved: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Feature engineering for ETF/PEA project"
    )
    parser.add_argument(
        "--ticker", type=str, required=True, help="Ticker symbol, e.g., 'EWLD.PA'"
    )
    parser.add_argument(
        "--window_fwd",
        type=int,
        default=30,
        help="Window forward for target calculation",
    )
    args = parser.parse_args()

    main(args.ticker, args.window_fwd)
