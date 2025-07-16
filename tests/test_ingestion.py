from pathlib import Path


def test_raw_files_exist():
    raw_path = Path("data/raw")
    parquet_files = list(raw_path.glob("*.parquet"))
    assert len(parquet_files) > 0, "Pas de fichiers parquet dans data/raw"
