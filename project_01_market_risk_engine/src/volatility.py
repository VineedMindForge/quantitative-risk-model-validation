import pandas as pd
import numpy as np

def historical_volatility(
    returns: pd.DataFrame,
    annualize: bool = True,
    periods_per_year: int = 252
)-> pd.Series:
    """
    Calculate historical volatility from asset returns.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame containing asset returns.
    annualize : bool, default=True
        Whether to annualize the volatility estimate.
    periods_per_year : int, default=252
        Number of observations per year.

    Returns
    -------
    pd.Series
        Volatility estimate for each asset.
    """
    
    volatility = returns.std()
    
    if annualize:
        volatility *= np.sqrt(periods_per_year)
        
    return volatility

def rolling_volatility(
    returns: pd.DataFrame,
    window: int = 60,
    annualize: bool = True,
    periods_per_year: int = 252
) -> pd.DataFrame:
    """
    Calculate rolling volatility from asset returns.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame containing asset returns.
    window : int, default=60
        Rolling estimation window.
    annualize : bool, default=True
        Whether to annualize the volatility estimate.
    periods_per_year : int, default=252
        Number of observations per year.

    Returns
    -------
    pd.DataFrame
        Rolling volatility for each asset.
    """

    volatility = returns.rolling(window=window).std()

    if annualize:
        volatility = volatility * np.sqrt(periods_per_year)

    return volatility


def ewma_volatility(
    returns: pd.DataFrame,
    lambda_: float = 0.94,
    annualize: bool = True,
    periods_per_year: int = 252
) -> pd.DataFrame:
    """
    Calculate EWMA volatility for multiple assets.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame containing asset returns.
    lambda_ : float, default=0.94
        EWMA decay factor.
    annualize : bool, default=True
        Whether to annualize the volatility estimate.
    periods_per_year : int, default=252
        Number of observations per year.

    Returns
    -------
    pd.DataFrame
        EWMA volatility estimates for each asset.
    """

    if not 0 < lambda_ < 1:
        raise ValueError("lambda_ must be between 0 and 1.")

    ewma_volatility = pd.DataFrame(
        index=returns.index,
        columns=returns.columns,
        dtype=float
    )

    for ticker in returns.columns:

        variance = np.zeros(len(returns))

        # Initial variance estimate
        variance[0] = returns[ticker].iloc[0] ** 2

        # EWMA recursion
        for i in range(1, len(returns)):

            variance[i] = (
                lambda_ * variance[i - 1]
                + (1 - lambda_) * returns[ticker].iloc[i - 1] ** 2
            )

        volatility = np.sqrt(variance)

        if annualize:
            volatility = volatility * np.sqrt(periods_per_year)

        ewma_volatility[ticker] = volatility

    return ewma_volatility
