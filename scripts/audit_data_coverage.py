#!/usr/bin/env python3
"""Provider-agnostic local CSV coverage audit; no network calls or legal conclusions."""
from __future__ import annotations
import argparse, json, re, unicodedata
from datetime import date, datetime
from pathlib import Path
import pandas as pd

def load(path, required, label):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"{label} CSV missing columns: {', '.join(sorted(missing))}")
    return df

def parsed_utc(series):
    return pd.to_datetime(series.replace("", pd.NA), errors="coerce", utc=True)

def normalize_headline(value):
    value = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", value)).strip()

def audit_news(path):
    df = load(path, {"ticker", "headline", "published_at"}, "News")
    df["ticker"] = df.ticker.str.upper().str.strip()
    df["published"] = parsed_utc(df.published_at)
    df["year"] = df.published.dt.year
    df["normalized"] = df.headline.map(normalize_headline)
    df["has_time"] = df.published_at.map(lambda x: bool(re.search(r"(?:T|\s)\d{1,2}:\d{2}", x)))
    df["missing_headline"] = df.headline.str.strip().eq("")
    df["bad_timestamp"] = df.published.isna()
    valid = df[df.year.notna()]
    rows = []
    for (ticker, year), group in valid.groupby(["ticker", "year"]):
        dup = group.duplicated(["ticker", "normalized", "published"])
        row = {"ticker": ticker, "year": int(year), "headline_rows": len(group),
               "unique_normalized_headlines": group.loc[~dup, "normalized"].nunique(),
               "duplicate_rows": int(dup.sum()), "missing_headline_rows": int(group.missing_headline.sum()),
               "valid_timestamp_rows": int((~group.bad_timestamp).sum()),
               "timestamp_completeness": round(float((~group.bad_timestamp).mean()), 4),
               "timestamps_with_clock_time": int(group.has_time.sum()),
               "clock_time_precision_rate": round(float(group.has_time.mean()), 4)}
        for col in ("publisher", "url", "first_seen_at"):
            if col in group:
                row[f"{col}_present_rows"] = int(group[col].str.strip().ne("").sum())
        rows.append(row)
    cols = ["ticker", "year"]
    summary = pd.DataFrame(rows).sort_values(cols) if rows else pd.DataFrame()
    return summary, {"rows_total": len(df), "valid_publication_timestamps": int(df.published.notna().sum()),
        "missing_or_invalid_timestamps": int(df.bad_timestamp.sum()), "missing_headlines": int(df.missing_headline.sum()),
        "rows_with_clock_time": int(df.has_time.sum()), "tickers": sorted(df.ticker.unique().tolist()),
        "duplicate_rule": "ticker + normalized headline + parsed publication timestamp",
        "caveat": "Clock-time presence is only a precision proxy; it does not prove timestamp accuracy or timezone correctness."}

def audit_prices(path):
    df = load(path, {"ticker", "date", "adjusted_close"}, "Prices")
    df["ticker"] = df.ticker.str.upper().str.strip()
    df["session"] = pd.to_datetime(df.date, errors="coerce").dt.date
    df["close"] = pd.to_numeric(df.adjusted_close, errors="coerce")
    bad = df.session.isna() | df.close.isna() | (df.close <= 0)
    valid = df.loc[~bad].copy()
    valid["year"] = pd.to_datetime(valid.session.astype(str)).dt.year
    spy = set(valid.loc[valid.ticker.eq("SPY"), "session"])
    rows = []
    for (ticker, year), group in valid.groupby(["ticker", "year"]):
        dates = set(group.session)
        expected = {d for d in spy if d.year == int(year)}
        rows.append({"ticker": ticker, "year": int(year), "valid_rows": len(group),
            "unique_sessions": len(dates), "spy_reference_sessions": len(expected),
            "missing_vs_spy_sessions": len(expected - dates) if ticker != "SPY" else 0,
            "coverage_vs_spy": round(len(dates & expected) / len(expected), 4) if expected else None,
            "duplicate_date_rows": int(group.duplicated(["session"]).sum())})
    summary = pd.DataFrame(rows).sort_values(["ticker", "year"]) if rows else pd.DataFrame()
    return summary, {"rows_total": len(df), "invalid_date_or_price_rows": int(bad.sum()),
        "spy_reference_sessions": len(spy), "tickers": sorted(df.ticker.unique().tolist()),
        "adjustment_caveat": "Column name does not verify split/dividend adjustment; confirm provider methodology.",
        "calendar_caveat": "SPY observed dates are a proxy, not a full exchange calendar or proof of ticker-specific missing data."}

def audit_membership(path, study_start, study_end):
    df = load(path, {"ticker", "start_date", "end_date"}, "Membership")
    df["ticker"] = df.ticker.str.upper().str.strip()
    df["start"] = pd.to_datetime(df.start_date, errors="coerce").dt.date
    df["end"] = pd.to_datetime(df.end_date, errors="coerce").dt.date
    start, end = date.fromisoformat(study_start), date.fromisoformat(study_end)
    invalid = df.start.isna() | df.end.isna()
    invalid |= df.apply(lambda r: bool(pd.notna(r.start) and pd.notna(r.end) and r.start > r.end), axis=1)
    good = df.loc[~invalid].copy()
    good["overlap"] = good.apply(lambda r: r.start <= end and r.end >= start, axis=1)
    active = good[good.overlap]
    rows = []
    for ticker, group in active.groupby("ticker"):
        intervals = sorted(zip(group.start, group.end))
        overlaps = sum(b[0] <= a[1] for a, b in zip(intervals, intervals[1:]))
        rows.append({"ticker": ticker, "interval_count": len(intervals),
            "first_membership_date": min(x[0] for x in intervals).isoformat(),
            "last_membership_date": max(x[1] for x in intervals).isoformat(),
            "overlapping_intervals": overlaps})
    summary = pd.DataFrame(rows).sort_values("ticker") if rows else pd.DataFrame()
    return summary, {"rows_total": len(df), "invalid_intervals": int(invalid.sum()),
        "valid_intervals_overlapping_study_period": len(active),
        "tickers_with_intervals": sorted(active.ticker.unique().tolist()),
        "caveat": "Interval coverage is not proof of completeness; independently verify dated additions/removals against authoritative evidence."}

def audit_manifest(path):
    df = load(path, {"source_id", "data_type", "provider", "dataset", "license_status"}, "Manifest")
    status = df.license_status.str.strip().str.lower()
    redist = df.get("redistribution_status", pd.Series(["unknown"] * len(df))).str.lower().str.strip()
    return df, {"source_rows": len(df), "license_status_counts": status.value_counts().to_dict(),
        "sources_marked_approved_by_researcher": int(status.isin({"approved", "verified"}).sum()),
        "redistribution_explicitly_allowed": int(redist.isin({"allowed", "permitted"}).sum()),
        "caveat": "Manifest values are researcher-entered; this script cannot interpret contracts or grant legal approval."}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--news", required=True); p.add_argument("--prices", required=True)
    p.add_argument("--membership", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--study-start", default="2018-01-01"); p.add_argument("--study-end", default="2025-12-31")
    p.add_argument("--output", default="outputs/coverage_audit")
    a = p.parse_args()
    nt, nm = audit_news(a.news); pt, pm = audit_prices(a.prices)
    mt, mm = audit_membership(a.membership, a.study_start, a.study_end)
    mf, mfm = audit_manifest(a.manifest)
    out = Path(a.output); out.mkdir(parents=True, exist_ok=True)
    for name, frame in {"news_coverage_by_ticker_year": nt, "price_coverage_by_ticker_year": pt,
        "membership_by_ticker": mt, "source_manifest_audited": mf}.items():
        frame.to_csv(out / f"{name}.csv", index=False)
    metadata = {"generated_at": datetime.now().astimezone().isoformat(),
        "study_period": {"start": a.study_start, "end": a.study_end},
        "news": nm, "prices": pm, "membership": mm, "manifest": mfm}
    (out / "audit_summary.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    report = ["# Data coverage pilot report", "", f"Generated: {metadata['generated_at']}", "",
        "> Descriptive input audit only. It does not assess predictive performance or approve providers.", "",
        "## News", "", f"- Rows: {nm['rows_total']}", f"- Valid timestamps: {nm['valid_publication_timestamps']}",
        f"- Missing/invalid timestamps: {nm['missing_or_invalid_timestamps']}", f"- Missing headlines: {nm['missing_headlines']}",
        f"- Rows with clock time: {nm['rows_with_clock_time']}", "", "See news_coverage_by_ticker_year.csv.", "",
        "## Adjusted prices", "", f"- Rows: {pm['rows_total']}", f"- Invalid rows: {pm['invalid_date_or_price_rows']}",
        f"- SPY reference sessions: {pm['spy_reference_sessions']}", "", pm["adjustment_caveat"], pm["calendar_caveat"],
        "", "See price_coverage_by_ticker_year.csv.", "", "## Historical membership", "",
        f"- Input intervals: {mm['rows_total']}", f"- Invalid intervals: {mm['invalid_intervals']}",
        f"- Intervals overlapping study period: {mm['valid_intervals_overlapping_study_period']}", "",
        mm["caveat"], "", "See membership_by_ticker.csv.", "", "## Licensing", "",
        f"- Manifest rows: {mfm['source_rows']}", f"- Sources marked approved by researcher: {mfm['sources_marked_approved_by_researcher']}",
        f"- Redistribution explicitly allowed: {mfm['redistribution_explicitly_allowed']}", "", mfm["caveat"], "",
        "No provider approval or empirical performance conclusion is produced."]
    (out / "pilot_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Audit written to {out.resolve()}")
    print("No provider approval or predictive-performance conclusion is produced.")

if __name__ == "__main__":
    main()
