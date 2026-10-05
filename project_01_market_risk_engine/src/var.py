import pandas as pd

def historical_var(
    returns: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float | None = None
) -> float:
    """Calculate Historical Value at Risk.

    Args:
        returns (pd.Series): Historical portfolio returns.
        confidence_level (float, optional): VaR confidence level.. Defaults to 0.95.
        portfolio_value (float | None, optional): Portfolio market value. If provided, VaR is returned in currency
        units. Otherwise, VaR is returned as a decimal percentage.. Defaults to None.

    Returns:
        float: Historical VaR expressed as a positive loss.
    """
    
    if not 0 < confidence_level <1.0:
        raise ValueError ("Confidence Interval Must be between 0 and 1")
    
    if returns.empty:
        raise ValueError("Returns cannot be empty.")
    
    if portfolio_value is not None and portfolio_value <= 0:
        raise ValueError("Portfolio_value must be greater than zero.")

    percentile = 1 - confidence_level

    return_quantile = returns.quantile(percentile)

    var = -return_quantile

    if portfolio_value is not None:
        var = var * portfolio_value

    return var
    
    

def historical_expected_shortfall(
    returns: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float | None = None
) -> float:
    """
    Calculate Historical Expected Shortfall.

    Expected Shortfall is the average loss among observations
    that fall beyond the Historical VaR threshold.

    Parameters
    ----------
    returns : pd.Series
        Historical portfolio returns.
    confidence_level : float, default=0.95
        ES confidence level.
    portfolio_value : float, optional
        Portfolio market value. If provided, ES is returned in currency
        units. Otherwise, ES is returned as a decimal percentage.

    Returns
    -------
    float
        Historical Expected Shortfall expressed as a positive loss.
    """

    if not 0 < confidence_level < 1:
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    if returns.empty:
        raise ValueError(
            "returns cannot be empty."
        )

    if portfolio_value is not None and portfolio_value <= 0:
        raise ValueError(
            "portfolio_value must be greater than zero."
        )

    percentile = 1 - confidence_level

    var_return = returns.quantile(percentile)

    tail_returns = returns[returns <= var_return]

    expected_shortfall = -tail_returns.mean()

    if portfolio_value is not None:
        expected_shortfall = expected_shortfall * portfolio_value

    return expected_shortfall
    