from pathlib import Path
import pandas as pd
from scripts.audit_data_coverage import audit_membership, audit_news, audit_prices, normalize_headline

def test_normalize_headline():
    assert normalize_headline("Apple:  NEW Product!") == "apple new product"

def test_news_counts_duplicates_and_missing_values(tmp_path: Path):
    path = tmp_path / "news.csv"
    pd.DataFrame([
        {"ticker":"AAPL","headline":"Apple launches product","published_at":"2025-01-02T14:30:00Z"},
        {"ticker":"AAPL","headline":"APPLE launches product!","published_at":"2025-01-02T14:30:00Z"},
        {"ticker":"AAPL","headline":"","published_at":""},
    ]).to_csv(path, index=False)
    table, meta = audit_news(path)
    assert table.iloc[0]["duplicate_rows"] == 1
    assert meta["missing_headlines"] == 1
    assert meta["missing_or_invalid_timestamps"] == 1

def test_price_coverage_uses_spy_reference_dates(tmp_path: Path):
    path = tmp_path / "prices.csv"
    pd.DataFrame([
        {"ticker":"SPY","date":"2025-01-02","adjusted_close":"580"},
        {"ticker":"SPY","date":"2025-01-03","adjusted_close":"581"},
        {"ticker":"AAPL","date":"2025-01-02","adjusted_close":"240"},
    ]).to_csv(path, index=False)
    table, meta = audit_prices(path)
    row = table[table.ticker == "AAPL"].iloc[0]
    assert row["missing_vs_spy_sessions"] == 1
    assert row["coverage_vs_spy"] == 0.5
    assert meta["spy_reference_sessions"] == 2

def test_membership_invalid_and_overlapping_intervals(tmp_path: Path):
    path = tmp_path / "members.csv"
    pd.DataFrame([
        {"ticker":"AAPL","start_date":"2020-01-01","end_date":"2025-12-31"},
        {"ticker":"BAD","start_date":"2025-01-01","end_date":"2020-01-01"},
        {"ticker":"OLD","start_date":"2010-01-01","end_date":"2015-01-01"},
    ]).to_csv(path, index=False)
    table, meta = audit_membership(path, "2018-01-01", "2025-12-31")
    assert table.ticker.tolist() == ["AAPL"]
    assert meta["invalid_intervals"] == 1
