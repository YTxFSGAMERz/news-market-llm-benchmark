"""Market-model event-study helpers."""

import pandas as pd
import statsmodels.api as sm


def market_model_abnormal_returns(
    stock_returns: pd.Series,
    market_returns: pd.Series,
    estimation_mask: pd.Series,
) -> pd.Series:
    """Estimate alpha/beta on estimation dates and return abnormal returns.

    Inputs must share an aligned index. The caller is responsible for defining
    an estimation window that ends before the event window.
    """
    aligned = pd.concat(
        [stock_returns.rename("stock"), market_returns.rename("market")], axis=1
    ).dropna()
    mask = estimation_mask.reindex(aligned.index).fillna(False).astype(bool)
    train = aligned.loc[mask]
    if len(train) < 20:
        raise ValueError("At least 20 valid estimation observations are required.")
    x_train = sm.add_constant(train["market"])
    fit = sm.OLS(train["stock"], x_train).fit()
    x_all = sm.add_constant(aligned["market"], has_constant="add")
    expected = fit.predict(x_all)
    abnormal = aligned["stock"] - expected
    return abnormal.rename("abnormal_return")
