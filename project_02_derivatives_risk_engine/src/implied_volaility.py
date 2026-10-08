import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))


import numpy as np
from black_scholes import black_scholes_price
from scipy.optimize import brentq

def calculate_implied_volatility(
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        q: float,
        option_type: str,
        sigma_low: float = 1e-6,
        sigma_high: float = 5.0
) ->float:
    """
    Calculate implied volatility using Brent's root-finding method.

    Parameters
    ----------
    market_price : float
        Observed market option price.
    S : float
        Spot price of the underlying asset.
    K : float
        Option strike price.
    T : float
        Time to expiration in years.
    r : float
        Continuously compounded risk-free rate.
    q : float
        Continuously compounded dividend yield.
    option_type : str
        'call' or 'put'.
    sigma_low : float
        Lower volatility bound.
    sigma_high : float
        Upper volatility bound.

    Returns
    -------
    float
        Implied volatility.
    """
    def pricing_error(sigma):
        model_price = black_scholes_price(S, K, T, sigma, r, q, option_type)
        return model_price - market_price

    try:
        implied_vol = brentq(pricing_error, sigma_low, sigma_high)
        return implied_vol
    except ValueError:
        return np.nan
