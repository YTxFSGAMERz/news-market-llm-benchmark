"""Input and model-output schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class HeadlineRecord(BaseModel):
    headline_id: str
    ticker: str
    headline: str
    published_at: datetime
    source: str | None = None

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()


class SentimentResult(BaseModel):
    headline_id: str
    label: Literal["positive", "neutral", "negative"]
    confidence: float = Field(ge=0.0, le=1.0)
    model_name: str
    prompt_version: str
