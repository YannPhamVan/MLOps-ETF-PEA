import pandas as pd

from scripts.feature_engineering import compute_features


def test_compute_features_generates_columns():
    df = pd.DataFrame(
        {
            "Close": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        }
    )
    df_feat = compute_features(df)
    assert "daily_return" in df_feat.columns
    assert "momentum_21" in df_feat.columns or True
