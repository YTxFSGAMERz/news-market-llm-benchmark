"""Small transparent baselines; not intended as production sentiment models."""

import re

POSITIVE = {"beat", "beats", "growth", "upgrade", "surge", "profit", "record", "strong"}
NEGATIVE = {"miss", "misses", "downgrade", "fall", "plunge", "loss", "weak", "lawsuit"}


def lexicon_score(text: str) -> int:
    """Return positive-word count minus negative-word count."""
    words = re.findall(r"[a-z]+", text.lower())
    return sum(word in POSITIVE for word in words) - sum(
        word in NEGATIVE for word in words
    )


def lexicon_label(text: str) -> str:
    score = lexicon_score(text)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"
