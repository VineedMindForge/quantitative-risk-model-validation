import numpy as np

from .black_scholes import black_scholes_price
from .implied_volatility import calculate_implied_volatility


def revalue_portfolio(
        portfolio,
        spot,
        risk_free_rate,
        dividend_yield,
        contract_multiplier=100,
        volatility_shock=0.0,
        days_elapsed=0
        ):
    """
    Revalue an options portfolio under stressed market conditions.

    Parameters
    ----------
    portfolio : pandas.DataFrame
        Portfolio containing option positions and current market data.

    spot : float
        Stressed underlying asset price.

    risk_free_rate : float
        Continuously compounded risk-free interest rate.

    dividend_yield : float
        Continuously compounded dividend yield.

    contract_multiplier : int, default=100
        Number of underlying units represented by one option contract.

    volatility_shock : float, default=0.0
        Absolute change in implied volatility.

    days_elapsed : int, default=0
        Number of calendar days elapsed from the current valuation date.

    Returns
    -------
    float
        Stressed market value of the entire portfolio.
    """

    stressed_value = 0.0

    for _, row in portfolio.iterrows():

        # Calculate base implied volatility dynamically
        base_iv = calculate_implied_volatility(
            market_price=row["mid_price"],
            S=row["spot"],
            K=row["strike"],
            T=row["T"],
            r=risk_free_rate,
            q=dividend_yield,
            option_type=row["option_type"]
        )

        if not np.isfinite(base_iv):
            raise ValueError(
                f"Unable to calculate implied volatility for "
                f"{row['option_type']} {row['strike']}"
            )

        # Apply volatility shock
        stressed_sigma = base_iv + volatility_shock

        # Prevent invalid volatility
        if stressed_sigma <= 0:
            stressed_sigma = 1e-6

        # Reduce time to expiration
        stressed_T = row["T"] - days_elapsed / 365

        # Handle expiration
        if stressed_T <= 0:

            if row["option_type"].lower() == "call":
                stressed_price = max(
                    spot - row["strike"],
                    0
                )

            elif row["option_type"].lower() == "put":
                stressed_price = max(
                    row["strike"] - spot,
                    0
                )

            else:
                raise ValueError(
                    "option_type must be either 'call' or 'put'"
                )

        else:

            stressed_price = black_scholes_price(
                S=spot,
                K=row["strike"],
                T=stressed_T,
                r=risk_free_rate,
                q=dividend_yield,
                sigma=stressed_sigma,
                option_type=row["option_type"]
            )

        # Aggregate signed position value
        stressed_value += (
            row["quantity"]
            * stressed_price
            * contract_multiplier
        )

    return stressed_value