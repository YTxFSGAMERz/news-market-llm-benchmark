# Data-source audit (research planning, 2026-11-10)

This is a candidate-source review, not proof that any provider is approved. Before acquiring data at scale, verify current endpoint entitlements, per-ticker coverage, timestamp semantics, and the actual license/contract.

## Executive recommendation

No verified zero-cost combination has yet been established that provides timestamped historical financial-news headlines, adjusted daily prices, and point-in-time S&P 100 membership for the entire proposed 2018-2025 period.

Run a small coverage and licensing pilot first:

1. Test Financial Modeling Prep (FMP) historical stock news for 2019 onward and confirm exact endpoint access under a selected plan.
2. Test one price provider for the stocks and SPY, checking adjusted close, splits, dividends, missing sessions, and historical depth.
3. Obtain dated S&P 100 membership history. If it cannot be sourced or reconstructed from dated official notices, do not claim survivorship-bias-free membership.
4. Keep raw news text and provider data private unless the license explicitly permits redistribution. Publish code, schemas, hashes, and permitted aggregate results.

## Candidate comparison

| Source | Coverage / access found | Cost signal | Main limitation | Provisional role |
|---|---|---|---|---|
| FMP Stock News | FMP says news for most symbols begins in 2019; some symbols have older coverage | Basic $0 / 250 calls per day; Starter $19/month billed annually; Premium $49/month billed annually | Per-symbol depth varies; verify exact endpoint entitlement and timestamp quality. Redistribution/display may require a separate agreement | Leading historical-news pilot candidate |
| NewsAPI | Developer searches up to one month; Business advertises up to five years | Developer free; Business listed at $449/month | Free tier is too shallow. Terms restrict republishing copyrighted material and building a competing news database | Not recommended as default |
| GDELT 2.0 | Global news monitoring and archive files; data access described as free/open | Free; attribution required | Not a clean issuer-headline archive. Validate headline availability and distinguish publisher timestamp from GDELT first-seen/ingestion timestamp | Auxiliary coverage, attention, and event features |
| SEC EDGAR | Official filing submissions and documents; public APIs and bulk archives | Free API access; no API key | Regulatory disclosures, not general financial news. Filing acceptance time must be treated carefully | Separate disclosure-event corpus |
| Alpha Vantage | Daily and adjusted daily OHLCV; docs describe 25+ years | Daily Adjusted endpoint marked premium | Confirm current quotas and plan entitlement for 100+ tickers | Market-price candidate |
| FMP EOD | Historical EOD prices | Basic lists EOD access; Premium lists 30+ years | Confirm adjusted fields, bulk access, and depth for selected plan | Convenient single-vendor price candidate |
| Nasdaq Data Link / Sharadar SEP | Adjusted/unadjusted EOD, corporate actions and reference data; coverage described from 1998 | Premium dataset; pricing requires account/quote | Paid; confirm publication/derived-data rights | Strong paid research-data candidate |
| yfinance / Yahoo Finance | Convenient Python access to Yahoo Finance history | Open-source client | Its documentation says Yahoo's API is intended for personal use; not a safe assumption for public redistribution | Exploratory local sanity checks only, subject to Yahoo terms |
| S&P Dow Jones Indices | Official S&P 100 description, methodology, and licensed constituent-data products | Historical constituent data is part of licensed data packages | Current constituents are not historical membership | Preferred authoritative membership source if licensing is feasible |
| Community constituent CSVs | Public S&P 500 historical membership projects exist | Public repositories | Not an authoritative S&P 100 history; provenance and completeness vary | Research lead only; validate independently |

## News sources

- FMP pricing: https://site.financialmodelingprep.com/pricing-plans
- FMP FAQ on stock-news history: https://site.financialmodelingprep.com/faqs?code=calendar
- NewsAPI pricing: https://newsapi.org/pricing
- NewsAPI terms: https://newsapi.org/terms
- GDELT data access: https://gdeltproject.org/data.html
- GDELT DOC API documentation: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

FMP's FAQ says stock news for most symbols begins in 2019, while some symbols may have older coverage. That makes 2019 a more defensible starting candidate than 2018 if FMP is selected, but it does not prove complete S&P 100 coverage. Measure coverage per ticker before changing the protocol.

NewsAPI's free Developer plan only searches articles up to one month old. Its paid Business tier advertises up to five years, currently listed at $449/month. Its terms restrict republication of copyrighted content and building a competing news database.

GDELT is useful for broad global coverage and attention/event features, but should not be treated as interchangeable with a curated financial-news headline feed. Validate which timestamp is original publication time versus first-seen/ingestion time. Do not label ingestion time as publisher time.

SEC EDGAR provides official issuer disclosures through free APIs and bulk archives. It can support a separate experiment on regulatory filing disclosures, but it is not a general financial-news headline source.

## Market-price sources

- Alpha Vantage docs: https://www.alphavantage.co/documentation/
- FMP pricing: https://site.financialmodelingprep.com/pricing-plans
- Nasdaq Data Link Sharadar SEP: https://data.nasdaq.com/databases/SEP/documentation
- yfinance docs and data-use disclaimer: https://ranaroussi.github.io/yfinance/

Alpha Vantage documents 25+ years of daily history, but its Daily Adjusted endpoint is marked premium. FMP advertises EOD data on its free tier and 30+ years on Premium; verify adjusted fields and actual access. Sharadar SEP is a research-oriented paid option with corporate-action and reference data. yfinance is convenient for exploratory checks, but its documentation says Yahoo's API is intended for personal use.

Use one provider for all stocks and SPY wherever possible. Record whether prices are raw, split-adjusted, or split-and-dividend-adjusted. Do not mix adjusted-close definitions across vendors.

## Historical index membership

- S&P 100 official page: https://www.spglobal.com/spdji/en/indices/equity/sp-100/
- S&P U.S. Indices methodology: https://www.spglobal.com/spdji/en/methodology/article/sp-us-indices-methodology/
- S&P data/index licensing: https://www.spglobal.com/spdji/en/about-us/data-index-licensing/
- Example community S&P 500 history project (not S&P 100): https://github.com/thuningxu/sp500nq100

S&P describes the S&P 100 as 100 companies selected from the S&P 500, generally larger companies with listed options, with sector balance considered. S&P's licensing page lists constituent data and corporate-action information among licensed data packages. A current constituent list must not be backfilled across the study period.

A public S&P 500 history file is not a valid substitute for S&P 100 history. If historical S&P 100 membership cannot be obtained, either secure a licensed source, reconstruct dated membership from official S&P announcements and independently validate every change, or switch to a fixed ticker basket and disclose survivorship limitations. Never claim point-in-time membership without evidence.

## Proposed coverage pilot

Before buying a subscription, test 10 liquid tickers across sectors plus SPY:

- News: sample at least 20 randomly selected trading dates per year per ticker. Record result count, publisher, headline, canonical URL, source timestamp, timezone, and first-seen timestamp if available.
- Prices: compare adjusted daily series over the full proposed period; inspect missing sessions, splits, dividends, delistings, and symbol changes.
- Membership: obtain dated S&P 100 additions/removals and verify that sampled membership intervals can be reconstructed.
- Legal: save exact plan terms and license/version date. Confirm whether storing headlines, model outputs, and derived statistics in a public repository is permitted.
- Reproducibility: save scripts, request parameters, retrieval date, dataset hashes, schema version, and source manifest. Keep restricted payloads out of Git.

If FMP is selected and coverage begins in 2019 for most symbols, consider changing the study window to 2019-01-01 onward only after the pilot. Do not change it merely because the provider's marketing page says "historical."

## Current decision

**No provider is approved yet.** FMP is the leading low-cost historical-news pilot candidate; Alpha Vantage, FMP EOD, and Sharadar are market-price candidates; S&P's licensed constituent data is the cleanest membership path. GDELT and SEC EDGAR are useful supplementary corpora with different semantics.

The next implementation task is a coverage-audit script and machine-readable source manifest, not bulk downloading.
