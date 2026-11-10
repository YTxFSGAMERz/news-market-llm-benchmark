from news_market_benchmark.baselines import lexicon_label, lexicon_score


def test_lexicon_score_and_label():
    assert lexicon_score("Strong profit growth") > 0
    assert lexicon_label("Company reports a loss") == "negative"
    assert lexicon_label("Company announces meeting") == "neutral"
