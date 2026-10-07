import numpy as np
from scipy.stats import norm

def black_scholes_price(

        S: float, 
        K: float, 
        T: float, 
        r: float, 
        q: float, 
        sigma: float,
        option_type: str, 
    ) ->float:
    """Calculate the Black-Scholes European option price with continuous dividend yield.

    Args:
        S (float): Current price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to maturity in years. Divide by 365 if input is in days.
        r (float): Annualized risk-free interest rate (decimal, e.g., 0.05 for 5%).
        q (float): Annualized continuous dividend yield (decimal, e.g., 0.02 for 2%).
        sigma (float): Annualized volatility of the underlying asset (decimal, e.g., 0.20 for 20%).
        option_type (str): Type of option; must be either 'call' or 'put'.

    Raises:
        ValueError: If `option_type` is not 'call' or 'put'.

    Returns:
        float: Theoretical price of the European option.
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price