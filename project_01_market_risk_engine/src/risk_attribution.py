import pandas as pd
from scipy.stats import norm

def marginal_var(
    covariance_matrix: pd.DataFrame,
    weights: pd.Series,
    portfolio_volatility: float,
    portfolio_mean_return: float,
    confidence_level: float = 0.95
) -> pd.Series:
    """Calculate Parametric Marginal VaR (MVaR) for each asset in a portfolio.

    Marginal VaR measures the rate of change of portfolio Value at Risk (VaR)
    with respect to a small change in the portfolio weight of an individual asset.

    Args:
        covariance_matrix (pd.DataFrame): Covariance matrix of asset daily returns, 
            indexed and columned by ticker symbol.
        weights (pd.Series): Portfolio weights for each asset, indexed by ticker symbol.
        portfolio_volatility (float): Total standard deviation (volatility) of the portfolio returns.
        portfolio_mean_returns (float): Expected portfolio return (mean of historical portfolio returns).
        confidence_level (float, optional): Confidence level for VaR calculation (e.g., 0.95 for 95%). 
            Defaults to 0.95.

    Returns:
        pd.Series: Marginal VaR for each asset, indexed by ticker symbol.
    """
    
    marginal_volatility = ( covariance_matrix @ weights ) / portfolio_volatility
    z_score = norm.ppf(1-confidence_level)
    mvar = -(portfolio_mean_return + z_score * marginal_volatility )
    
    return mvar

def component_var(
    weights: pd.Series,
    marginal_var_values: pd.Series
) -> pd.Series:
    """Calculate Component VaR for each asset in a portfolio.

Component VaR measures the contribution of each asset to total portfolio VaR,
computed as the product of the asset's portfolio weight and its Marginal VaR.

The sum of all Component VaRs equals total portfolio VaR under Euler decomposition.

    Args:
        weights (pd.Series): Portfolio weights for each asset, indexed by ticker symbol.
        marginal_var_values (pd.Series): Marginal VaR values for each asset, 
            indexed by ticker symbol.

    Returns:
        pd.Series: Component VaR for each asset, indexed by ticker symbol.
    """
    
    return weights * marginal_var_values

def var_contribution(
    component_var_values: pd.Series
) -> pd.Series:
    """Calculate the percentage contribution to total portfolio VaR for each asset.

    Calculates the relative proportion of total portfolio risk contributed by 
    each asset. The resulting percentages sum to 1.0 (100%).

    Args:
        component_var_values (pd.Series): Component VaR values for each asset, 
            indexed by ticker symbol.

    Returns:
        pd.Series: Percentage contribution of each asset to total portfolio VaR.
    """
    
    return component_var_values / component_var_values.sum()