# Methodology (protocol draft v0.1)

## Scope and unit of analysis

The first experiment studies US-listed equities from 2018-01-01 through 2025-12-31. The proposed universe is the S&P 100, using point-in-time membership. A current constituent list must not be backfilled across the full period because doing so creates survivorship bias. If reliable historical membership cannot be obtained, the study must be relabeled as a fixed-universe exploratory analysis and its limitation disclosed.

The India extension will use NIFTY 50 constituents and will be run as a separate market study after the US pipeline is stable. Do not combine the markets in the primary result.

One observation is a timestamped headline confidently mapped to one issuer/ticker. Retain source, canonical URL, original timestamp, timezone, normalized UTC timestamp, retrieval timestamp, and duplicate-group ID.

## Primary target

For each eligible headline, calculate the stock's return from the last regular-session close before publication to the close of the next eligible regular session. Subtract the corresponding SPY benchmark return:

    excess_return = stock_return - SPY_return

The binary target is 1 for strictly positive excess return and 0 otherwise. A headline after the regular close, on a weekend, or on an exchange holiday maps to the next eligible session. A pre-market headline maps to that session only when its verified timestamp precedes the regular open. Ambiguous/date-only timestamps are excluded from the primary analysis and counted in the exclusion report.

This is a predictive association, not evidence that a headline caused a return.

## Data quality and entity resolution

Use a documented ticker/issuer alias dictionary. Manually review ambiguous mappings without consulting future outcomes. Deduplicate exact and near-duplicate/syndicated headlines and keep related duplicates in one split. Preserve an exclusion reason for every discarded record. Never infer publication time from retrieval time.

## Models

- Market-only baseline: lagged returns and volume features available before publication.
- Lexicon baseline: transparent repository implementation.
- FinBERT: fixed checkpoint/tokenizer revision, recorded in run metadata.
- LLMs: fixed model identifier, prompt version, parameters, response schema, and request date.

All text classifiers receive identical headline text. Keep three-class sentiment (positive/neutral/negative) and document the conversion to a numeric score. No prompt or threshold tuning on the final test set.

## Time splits

- Train: 2018-01-01 to 2022-12-31
- Validation: 2023-01-01 to 2024-12-31
- Test: 2025-01-01 to 2025-12-31

Use chronological splits only. Fit learned preprocessing on training data. Freeze prompts and model versions before evaluating the test period. Keep duplicate groups inside one split.

## Metrics and inference

Primary metric: ROC-AUC for positive next-session excess return. Report sample count and class balance. Secondary metrics include accuracy, balanced accuracy, precision, recall, F1, Brier score, and calibration where probabilities are available. Compare models on identical observations and report confidence intervals.

Event studies are secondary. Estimate expected returns with a market model over a pre-event estimation window that does not overlap the event window. Freeze exact windows before examining test outcomes. Report abnormal and cumulative abnormal returns with uncertainty intervals. Account for repeated ticker/date observations using an explicitly documented clustered or block-bootstrap method, and correct secondary hypothesis families for multiple comparisons.

## Data-source selection

Candidate news sources include GDELT 2.0, issuer press-release archives, and licensed financial-news datasets. Candidate market data must provide documented adjusted OHLCV history and clear terms; use one provider for equities and SPY where possible. Historical S&P 100 membership requires a dated, verifiable source. These are candidates, not approved sources.

Before freezing the protocol, audit coverage, timestamp precision/timezone, corporate-action treatment, historical constituent coverage, API limits, costs, licenses, and redistribution restrictions. Keep restricted raw data out of Git. Do not treat a free endpoint as permission to redistribute its data.

## Limitations

Headline sentiment is not market surprise. Returns may reflect expectations, concurrent news, macroeconomic conditions, liquidity, and information already priced in. Survivorship bias, timestamp errors, corporate actions, and data-mining can distort findings. Report null and negative results.
