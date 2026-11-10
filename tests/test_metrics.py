from news_market_benchmark.metrics import classification_metrics


def test_metrics_include_auc_when_both_classes_present():
    result = classification_metrics([0, 1, 1], [0, 1, 0], [0.1, 0.9, 0.4])
    assert result["accuracy"] == 2 / 3
    assert result["roc_auc"] is not None


def test_auc_is_none_for_single_class():
    result = classification_metrics([1, 1], [1, 0], [0.8, 0.2])
    assert result["roc_auc"] is None
