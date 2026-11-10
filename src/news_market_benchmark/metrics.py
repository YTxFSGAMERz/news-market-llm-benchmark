"""Classification metrics with safe handling of single-class targets."""

from collections.abc import Sequence

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(
    y_true: Sequence[int], y_pred: Sequence[int], y_score: Sequence[float] | None = None
) -> dict[str, float | None]:
    result: dict[str, float | None] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": None,
    }
    if y_score is not None and len(set(y_true)) == 2:
        result["roc_auc"] = float(roc_auc_score(y_true, y_score))
    return result
