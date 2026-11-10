# Preregistration protocol v0.1

**Status:** Proposed design. Data-source coverage, licensing, and point-in-time universe history must be audited before this protocol is frozen. No empirical results are available.

## 1. Research scope

- **Primary market:** US-listed equities.
- **Initial universe:** S&P 100 constituents, using historical point-in-time membership for each date wherever a verifiable membership history can be obtained.
- **Extension:** NIFTY 50 constituents in India, analyzed separately after the US pipeline is stable. Do not pool US and Indian observations in the primary analysis.
- **Proposed study period:** 2018-01-01 through 2025-12-31.
- **Unit of analysis:** one eligible, timestamped headline mapped to one issuer/ticker.
- **Primary benchmark:** SPY as a tradable proxy for the S&P 500. Record the exact price series and adjustment policy used.

A current constituent list must not be silently applied to the entire historical period. If point-in-time membership cannot be sourced, narrow the study to a clearly labeled fixed-universe exploratory analysis and quantify survivorship limitations.

## 2. Primary outcome

The primary target is the direction of the next eligible regular-session excess return:

    excess_return = stock_return - benchmark_return
    direction = 1 when excess_return > 0, otherwise 0

The return interval begins at the last regular-session close before the headline became public and ends at the close of the next eligible regular session. Headlines published after the regular close, on weekends, or on exchange holidays are assigned to the next eligible session. Pre-market headlines are eligible for that session only if their verified publication timestamp precedes the regular open. Headlines with ambiguous or date-only timestamps are excluded from the primary timestamp-sensitive analysis and counted in a data-quality report.

This is a predictive association target, not a causal claim or a trading strategy.

## 3. Headline eligibility and mapping

- Retain original publication timestamp, source, canonical URL, headline text, and retrieval timestamp.
- Normalize timestamps to UTC while retaining the source timezone and original timestamp.
- Map headlines to issuers using a documented deterministic alias/ticker dictionary; manually review ambiguous mappings without looking at future returns.
- Deduplicate exact and near-duplicate/syndicated headlines. Keep a stable duplicate-group ID.
- Exclude headlines that cannot be confidently mapped, lack a reliable publication timestamp, or were published after the relevant market reaction began.
- Preserve a provenance record for every exclusion.

## 4. Models and comparisons

1. **Market-only:** lagged returns and volume-derived features available before the headline.
2. **Lexicon baseline:** the repository's transparent lexical sentiment method.
3. **FinBERT:** fixed, documented checkpoint and tokenizer revision; record model hash/revision.
4. **LLM classifiers:** fixed provider/model identifier, prompt version, decoding parameters, response schema, and request date.

All text models receive the same eligible headline text. They must return positive, neutral, or negative sentiment plus a confidence/uncertainty field where supported. Define the mapping from three-class sentiment to a numeric score before evaluation. Do not tune prompts or thresholds on the final test period.

## 5. Chronological evaluation

Proposed split by publication date:
- Train: 2018-01-01 to 2022-12-31
- Validation: 2023-01-01 to 2024-12-31
- Test: 2025-01-01 to 2025-12-31

The split dates are calendar-based and must be applied consistently to all models. Fit learned preprocessing and thresholds on training/validation only. Keep the test set untouched until the protocol, prompts, and model versions are frozen. Keep duplicate groups within a single split.

## 6. Primary and secondary metrics

Primary metric: ROC-AUC for predicting positive next-session excess return. Report the number of observations and class balance alongside it.

Secondary metrics: accuracy, balanced accuracy, precision, recall, F1, Brier score, calibration where probabilities are available, and performance by year/sector. Include confidence intervals and compare models on the same observations.

## 7. Event study and inference

The event-study analysis is secondary to the predictive classification task. Use a market model estimated over a pre-event window that does not overlap the event window. Predeclare estimation and event windows in the frozen protocol before inspecting test outcomes.

Report abnormal returns and cumulative abnormal returns with confidence intervals. Account for dependence from repeated tickers and common calendar dates using an appropriate clustered or block-bootstrap procedure. State the method and its limitations. Correct secondary hypothesis families for multiple comparisons.

## 8. Data-source audit (required before freeze)

For each candidate source, record: provider, dataset/API and version, fields, timestamp precision and timezone, coverage, survivorship/constituent-history support, corporate-action treatment, rate limits, cost, license, redistribution restrictions, retrieval date, and known gaps.

Candidate discovery sources (not yet approved or guaranteed):
- News: GDELT 2.0, issuer press-release archives, and licensed financial-news datasets if access is available.
- Market data: a documented adjusted daily OHLCV provider with historical coverage and clear terms; SPY benchmark data from the same provider where possible.
- Universe history: an authoritative S&P 100 historical constituent source with dated additions/removals.

Do not assume search snippets, scraped copies, or a free API imply permission to redistribute data. Store raw licensed data outside Git and publish only metadata or derived data permitted by the license.

## 9. Robustness and limitations

Planned checks: alternative return horizons, raw versus benchmark-relative direction, neutral-sentiment handling, timestamp-quality exclusions, sector/year splits, and a survivorship-bias sensitivity analysis. Label all secondary analyses clearly.

Headline polarity is not the same as surprise. Market moves reflect expectations, other news, macroeconomic conditions, liquidity, and information already priced in. Correlation does not establish causation.

## 10. Reproducibility and deviations

Record code commit, environment lockfile, dataset version/hash, retrieval date, model identifier/revision, exact prompt, parameters, run timestamp, random seeds, exclusions, and output hashes. Never commit secrets or restricted raw data.

Complete the source audit and freeze this protocol before opening final test results. Date and explain every deviation; do not rewrite the protocol retrospectively to fit findings.
