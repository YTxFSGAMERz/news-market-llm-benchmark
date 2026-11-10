# Methodology (draft)

## Unit of analysis

One timestamped financial-news headline associated with one publicly traded ticker. Deduplication and entity mapping rules must be fixed before model evaluation.

## Outcome

The initial proposed outcome is the sign of the ticker's next tradable-session close-to-close return relative to a predeclared benchmark. The final definition must account for after-hours publication, exchange holidays, time zones and market opening times. Do not assign a same-day return to a headline published after the relevant price move.

## Models

1. Market-only baseline: lagged returns and volume-derived features.
2. Transparent lexical baseline.
3. FinBERT or another documented finance-domain classifier.
4. LLM classifiers with fixed prompts and recorded model versions.

All models receive the same eligible headline text. Any model-specific preprocessing must be documented.

## Splits and leakage

Use chronological splits by publication time. Fit all learned preprocessing on training data only. Keep the final test period untouched until model and prompt choices are frozen. Group duplicate or syndicated headlines to prevent near-identical text crossing splits.

## Event study

Estimate expected returns with a market model over a pre-event estimation window. Compute abnormal returns as observed minus expected returns. Aggregate abnormal returns over predeclared event windows. The estimation window must not overlap the event window.

## Statistical analysis

Report confidence intervals and effect sizes, not only p-values. Account for repeated observations by ticker and date where feasible. Predefine primary comparisons and correct for multiple testing when conducting families of secondary tests.

## Limitations

Headline sentiment is not the same as market surprise. Price reactions depend on expectations, macroeconomic conditions, liquidity, sector effects and information already priced in. Results may not generalize across markets or periods.
