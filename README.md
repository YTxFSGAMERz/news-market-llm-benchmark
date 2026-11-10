# When LLMs Read the News

**Can text fix what numbers miss?** A reproducible research project testing whether language-model sentiment signals from financial news headlines contain information about subsequent stock-market reactions.

> Research status: scaffold and methodology in progress. No empirical findings are claimed. Synthetic sample data is provided only to test the pipeline.

## Research question

Do LLM-classified headline signals predict next-session market reactions better than simple text and price/volume baselines?

## Planned comparisons

- Lexicon sentiment baseline
- FinBERT financial sentiment baseline
- LLM sentiment classifiers (provider/model and exact prompt recorded)
- Market-only baseline using lagged returns and volume features

## Primary evaluation

- Direction classification: ROC-AUC, accuracy, precision, recall, F1
- Event study: market-model abnormal returns and cumulative abnormal returns
- Statistical inference: confidence intervals and tests with dependence-aware standard errors
- Robustness: alternative event windows, thresholds, sector splits and time-based holdouts

## Research integrity

1. A headline timestamp must precede the measured market reaction.
2. Use chronological train/validation/test splits. Never randomly mix future observations into training.
3. Keep prompt, model identifier, parameters, data version and run timestamp for every LLM result.
4. Do not tune on the final test set.
5. Report null and negative results.
6. Clearly distinguish synthetic examples from real observations.
7. Check licensing and terms for every dataset and model.

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

The starter validates input data and provides baseline metric/event-study utilities. It does not download market data or call paid LLM APIs.

## Coverage pilot

Use the provider-agnostic local CSV auditor before selecting a vendor. See [coverage audit instructions](docs/coverage_audit.md) and the [data-source audit](docs/data_sources.md). The auditor writes per-ticker/year news and price coverage, membership checks, a source-manifest copy, JSON summary, and Markdown report. It makes no network calls and does not approve providers.

## Input data

See [data dictionary](docs/data_dictionary.md). The sample CSV is synthetic. Keep licensed/raw datasets out of Git unless redistribution is explicitly permitted. Put local raw files in `data/raw/` (ignored by Git).

## Data-source audit

Candidate news, market-price, and index-membership sources have been compared, including access and licensing constraints. No provider is approved yet; see [data-source audit](docs/data_sources.md) before acquiring data.

## Initial protocol

The proposed first study is US equities (S&P 100, point-in-time membership) from 2018-01-01 to 2025-12-31, with a separate NIFTY 50 India extension later. The primary target is next-session stock excess-return direction versus SPY. This design remains provisional until news coverage, market-data quality, historical constituent membership, and licensing are audited. See [protocol v0.1](docs/preregistration.md).

## Research plan

See:
- [Methodology](docs/methodology.md)
- [Preregistration checklist](docs/preregistration.md)

## Project structure

```
src/news_market_benchmark/  # reusable Python package
tests/                      # unit tests
data/sample/                # synthetic test fixture only
data/raw/                   # local, untracked source data
data/processed/             # generated datasets
docs/                       # protocol and data documentation
```

## Responsible interpretation

This is an academic research experiment, not investment advice or a trading system. Predictive association does not establish causation, and backtest results can be distorted by survivorship bias, look-ahead leakage, transaction costs and data-mining.

## License

To be selected after dataset and contribution requirements are reviewed.
