import pandas as pd
from scipy.stats import norm
import numpy as np

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


def parametric_var(
    returns: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float |None = None
) -> float:
    """Calculate Parametric Value at Risk.

    Args:
        returns (pd.Series): Historical portfolio returns
        confidence_level (float, optional): VaR confidence level. Defaults to 0.95.
        portfolio_value (float | None, optional): Portfolio market value. If provided, VaR is returned in currency
                units. Otherwise, VaR is returned as a decimal percentage. Defaults to None.

    Returns:
        float: Parametric VaR expressed as a positive loss.
    """
    if not 0 < confidence_level <1.0:
        raise ValueError ("Confidence Interval Must be between 0 and 1")
    
    if returns.empty:
        raise ValueError("Returns cannot be empty.")
    
    if portfolio_value is not None and portfolio_value <= 0:
        raise ValueError("Portfolio_value must be greater than zero.")
    
    mu = returns.mean()
    sigma = returns.std()
    z_score = norm.ppf(1-confidence_level)
    
    var = -(mu +z_score*sigma)
    
    if portfolio_value is not None:
        var = var * portfolio_value
        
    return var

def monte_carlo_var(
    returns: pd.DataFrame,
    weights: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float | None = None,
    n_simulations: int = 100_000,
    random_seed: int | None = 42
) -> float:
    """Calculate Monte Carlo Value at Risk.

    Simulates correlated asset returns using historical mean returns
    and covariance, assuming normally distributed returns.

    Args:
        returns (pd.DataFrame): Historical asset returns.
        weights (pd.Series): Portfolio weights.
        confidence_level (float, optional): VaR confidence level. Defaults to 0.95.
        portfolio_value (float | None, optional): Portfolio market value. Defaults to None.
        n_simulations (int, optional): Number of Monte Carlo scenarios. Defaults to 100_000.
        random_seed (int | None, optional): Random seed for reproducibility. Defaults to 42.

    Returns:
        float: Monte Carlo VaR expressed as a positive loss.
    """
    if not 0 < confidence_level < 1.0:
        raise ValueError("Confidence level must be between 0 and 1.")

    if returns.empty:
        raise ValueError("Returns cannot be empty.")

    if portfolio_value is not None and portfolio_value <= 0:
        raise ValueError("Portfolio value must be greater than zero.")

    if n_simulations <= 0:
        raise ValueError("n_simulations must be greater than zero.")

    weights = weights.reindex(returns.columns)

    if weights.isna().any():
        raise ValueError("Weights must contain all return columns.")

    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.")
    
    mean_returns = returns.mean()
    covariance_matrix = returns.cov()
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    cholesky_matrix = np.linalg.cholesky(covariance_matrix)
    normal_simulated_shocks = np.random.normal(size = (n_simulations, len(returns.columns)))
    correlated_simulated_shocks = normal_simulated_shocks @ cholesky_matrix.T
    
    simulated_returns = correlated_simulated_shocks + mean_returns.values
    
    simulated_portfolio_returns = simulated_returns @ weights.values
    
    percentile = 1 - confidence_level
    
    var_return = np.quantile(simulated_portfolio_returns, percentile)
    var = - var_return
    
    if portfolio_value is not None:
        var *= portfolio_value

    return var

def monte_carlo_es(
    returns: pd.DataFrame,
    weights: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float | None = None,
    n_simulations: int = 100_000,
    random_seed: int | None = 42
) -> float:
    """Calculate Monte Carlo Expected Shortfall.

    Simulates correlated asset returns using historical mean returns
    and covariance, assuming normally distributed returns.

    Args:
        returns (pd.DataFrame): Historical asset returns.
        weights (pd.Series): Portfolio weights.
        confidence_level (float, optional): VaR confidence level. Defaults to 0.95.
        portfolio_value (float | None, optional): Portfolio market value. Defaults to None.
        n_simulations (int, optional): Number of Monte Carlo scenarios. Defaults to 100_000.
        random_seed (int | None, optional): Random seed for reproducibility. Defaults to 42.

    Returns:
        float: Monte Carlo ES expressed as a positive loss.
    """
    if not 0 < confidence_level < 1.0:
        raise ValueError("Confidence level must be between 0 and 1.")

    if returns.empty:
        raise ValueError("Returns cannot be empty.")

    if portfolio_value is not None and portfolio_value <= 0:
        raise ValueError("Portfolio value must be greater than zero.")

    if n_simulations <= 0:
        raise ValueError("n_simulations must be greater than zero.")

    weights = weights.reindex(returns.columns)

    if weights.isna().any():
        raise ValueError("Weights must contain all return columns.")

    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.")
    
    mean_returns = returns.mean()
    covariance_matrix = returns.cov()
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    cholesky_matrix = np.linalg.cholesky(covariance_matrix)
    normal_simulated_shocks = np.random.normal(size = (n_simulations, len(returns.columns)))
    correlated_simulated_shocks = normal_simulated_shocks @ cholesky_matrix.T
    
    simulated_returns = correlated_simulated_shocks + mean_returns.values
    
    simulated_portfolio_returns = simulated_returns @ weights.values
    
    percentile = 1 - confidence_level
    
    var_return = np.quantile(simulated_portfolio_returns, percentile)
    
    tail_return = simulated_portfolio_returns[simulated_portfolio_returns<var_return]
    
    es = -tail_return.mean()
    
    if portfolio_value is not None:
        es *= portfolio_value

    return es 
    
    
        
        
