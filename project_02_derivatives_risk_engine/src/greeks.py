import numpy as np
from scipy.stats import norm

def calculate_greeks(
        S: float, 
        K: float, 
        T: float, 
        r: float, 
        q: float, 
        sigma: float,
        option_type: str
        ) -> dict:
    """
    Calculate the Black-Scholes Greeks for a European call or put option.

    Parameters
    ----------
    S : float
        Current price of the underlying asset.
    K : float
        Strike price of the option.
    T : float
        Time to maturity in years.
    r : float
        Continuously compounded risk-free interest rate.
    q : float
        Continuous dividend yield.
    sigma : float
        Annualized volatility.
    option_type : str
        Option type: "call" or "put".

    Returns
    -------
    dict
        Dictionary containing Delta, Gamma, Vega, Theta, and Rho.
    """

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    pdf_d1 = norm.pdf(d1)
    cdf_d1 = norm.cdf(d1)
    cdf_d2 = norm.cdf(d2)

    if option_type.lower() == "call":
        delta = np.exp(-q * T) * cdf_d1
        gamma = np.exp(-q * T) * pdf_d1 / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * pdf_d1 * np.sqrt(T)
        theta = (
    -S * np.exp(-q * T) * pdf_d1 * sigma / (2 * np.sqrt(T))
    - r * K * np.exp(-r * T) * cdf_d2
    + q * S * np.exp(-q * T) * cdf_d1
)
        rho = K * T * np.exp(-r * T) * cdf_d2
    elif option_type.lower() == "put":
        delta = -np.exp(-q * T) * cdf_d1
        gamma = np.exp(-q * T) * pdf_d1 / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * pdf_d1 * np.sqrt(T)
        theta = (
    -S * np.exp(-q * T) * pdf_d1 * sigma / (2 * np.sqrt(T))
    + r * K * np.exp(-r * T) * (1 - cdf_d2)
    - q * S * np.exp(-q * T) * (1 - cdf_d1)
)
        rho = -K * T * np.exp(-r * T) * (1 - cdf_d2)

    else:
        raise ValueError("option_type must be either 'call' or 'put'")

        

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho
    }