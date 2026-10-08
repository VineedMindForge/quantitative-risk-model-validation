import numpy as np
from scipy.optimize import brentq

from .black_scholes import black_scholes_price


def calculate_implied_volatility(
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        q: float,
        option_type: str
        ) -> float:
    """
    Calculate the implied volatility of a European option.

    Parameters
    ----------
    market_price : float
        Observed market price of the option.

    S : float
        Current underlying asset price.

    K : float
        Option strike price.

    T : float
        Time to expiration in years.

    r : float
        Continuously compounded risk-free interest rate.

    q : float
        Continuously compounded dividend yield.

    option_type : str
        Option type: "call" or "put".

    Returns
    -------
    float
        Implied volatility.

    Notes
    -----
    Implied volatility is obtained by solving:

        Black-Scholes Price(sigma) = Market Price

    using Brent's root-finding algorithm.
    """

    if market_price <= 0:
        return np.nan

    if S <= 0 or K <= 0 or T <= 0:
        return np.nan

    option_type = option_type.lower()

    if option_type not in {"call", "put"}:
        raise ValueError(
            "option_type must be either 'call' or 'put'"
        )

    def objective_function(sigma):
        model_price = black_scholes_price(
            S=S,
            K=K,
            T=T,
            r=r,
            q=q,
            sigma=sigma,
            option_type=option_type
        )

        return model_price - market_price

    try:
        implied_volatility = brentq(
            objective_function,
            1e-6,
            5.0
        )

    except ValueError:
        return np.nan

    return implied_volatility
    