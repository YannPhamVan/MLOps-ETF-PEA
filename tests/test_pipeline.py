from pathlib import Path

import pandas as pd


def test_pipeline_creates_prediction_file():
    pred_path = Path("data/predictions/predictions.parquet")
    assert pred_path.exists(), "Le fichier de prédictions n'existe pas"
    df = pd.read_parquet(pred_path)
    assert not df.empty, "Le fichier de prédictions est vide"
