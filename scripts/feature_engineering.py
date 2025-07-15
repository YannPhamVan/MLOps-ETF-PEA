import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA_PATH = Path("../data/raw")
FEATURES_DATA_PATH = Path("../data/features")
FEATURES_DATA_PATH.mkdir(parents=True, exist_ok=True)

WINDOW_FWD = 30  # forward 30-day target

def compute_features(df):
    df = df.copy()

    df['daily_return'] = df['Close'].pct_change()
    df['weekly_return'] = df['Close'].pct_change(5)
    df['monthly_return'] = df['Close'].pct_change(21)

    df['rolling_volatility_21'] = df['daily_return'].rolling(21).std()
    df['rolling_volatility_63'] = df['daily_return'].rolling(63).std()

    df['momentum_21'] = df['Close'] / df['Close'].shift(21) - 1
    df['momentum_63'] = df['Close'] / df['Close'].shift(63) - 1

    df['ma_21'] = df['Close'].rolling(21).mean()
    df['ma_63'] = df['Close'].rolling(63).mean()

    rolling_max = df['Close'].rolling(252, min_periods=1).max()
    df['drawdown'] = df['Close'] / rolling_max - 1

    # ✅ Target
    df['target'] = df['Close'].pct_change(WINDOW_FWD).shift(-WINDOW_FWD)

    df = df.dropna()
    return df

def process_all_files():
    parquet_files = list(RAW_DATA_PATH.glob("*.parquet"))
    print(f"Found {len(parquet_files)} raw files.")
    for file in parquet_files:
        print(f">>> Processing {file.name}...")
        df = pd.read_parquet(file)
        df_features = compute_features(df)
        output_path = FEATURES_DATA_PATH / f"{file.stem}_features.parquet"
        df_features.to_parquet(output_path, index=False)
        print(f">>> Saved features to {output_path}")

if __name__ == "__main__":
    process_all_files()
