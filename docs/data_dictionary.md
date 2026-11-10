# Data dictionary

## Headline input CSV

| Column | Type | Meaning |
|---|---|---|
| headline_id | string | Unique stable identifier |
| ticker | string | Exchange ticker mapped to the headline |
| headline | string | Headline text only, unless protocol explicitly expands scope |
| published_at | ISO-8601 datetime | Original publication timestamp with timezone |
| source | string, optional | Publisher/source identifier |

## Required market data (planned)

| Field | Meaning |
|---|---|
| timestamp/date | Exchange-local trading date and/or timestamp |
| ticker | Security identifier |
| adjusted_close | Split/dividend-adjusted close |
| volume | Trading volume |
| market_return | Return for the predeclared benchmark |

Keep vendor, retrieval date, adjustment method, currency, exchange timezone and licensing details in dataset metadata. Synthetic examples are not research observations.
