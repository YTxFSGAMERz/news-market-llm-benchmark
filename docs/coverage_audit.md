# Reproducible data coverage pilot

The auditor reads local CSV extracts only. It makes no network requests, does not assess predictive performance, and cannot determine legal rights.

## Pilot design

Select 10 liquid US stocks across sectors plus SPY. Record the selection rule before checking provider coverage. For news, sample at least 20 randomly selected trading dates per year and ticker. Save the random seed, query parameters, retrieval date, and sampling frame. Do not silently replace poorly covered tickers.

## Input schemas

- News CSV: required columns ticker, headline, published_at. Optional publisher, url, first_seen_at, source_timezone.
- Adjusted-price CSV: required ticker, date (YYYY-MM-DD), adjusted_close. Optional adjustment_method and currency.
- Membership CSV: required ticker, start_date, end_date. Optional index_name and source_reference. Intervals are inclusive.
- Source manifest: start from data/sample/source_manifest_template.csv. Keep unknown rights as unknown/unverified.

Preserve original timestamp strings and timezone semantics. Clock-time presence is only a precision proxy, not proof of timestamp accuracy. Never substitute ingestion time for publication time.

## Run

```bash
python -m pip install -e ".[dev]"
python scripts/audit_data_coverage.py \
  --news data/raw/news_pilot.csv \
  --prices data/raw/adjusted_prices_pilot.csv \
  --membership data/raw/sp100_membership_pilot.csv \
  --manifest data/sample/source_manifest_template.csv \
  --study-start 2018-01-01 --study-end 2025-12-31
pytest
```

Outputs are written to outputs/coverage_audit/:
- news_coverage_by_ticker_year.csv
- price_coverage_by_ticker_year.csv
- membership_by_ticker.csv
- source_manifest_audited.csv
- audit_summary.json
- pilot_report.md

## Interpretation limits

1. Results describe only the supplied extracts and sampling design.
2. Duplicate detection uses ticker + normalized headline + parsed publication timestamp; syndicated copies with different timestamps may remain.
3. SPY dates are a proxy session calendar, not proof of valid trading dates for each security.
4. The adjusted_close column name does not prove split/dividend adjustment. Verify vendor methodology.
5. Membership intervals must be reconciled against authoritative dated additions/removals.
6. Manifest statuses are researcher-entered, not legal conclusions. Do not mark a source approved until the actual contract and terms are reviewed.
7. Keep licensed raw data out of public Git unless redistribution is explicitly permitted.
