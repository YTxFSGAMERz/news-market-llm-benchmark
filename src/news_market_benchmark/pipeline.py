"""CSV ingestion and validation helpers."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"headline_id", "ticker", "headline", "published_at"}


def load_headlines(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = frame.copy()
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    frame["published_at"] = pd.to_datetime(frame["published_at"], utc=True, errors="raise")
    if frame["headline_id"].duplicated().any():
        raise ValueError("headline_id values must be unique.")
    if frame["headline"].isna().any() or frame["ticker"].eq("").any():
        raise ValueError("headline and ticker must be non-empty.")
    return frame.sort_values("published_at").reset_index(drop=True)
