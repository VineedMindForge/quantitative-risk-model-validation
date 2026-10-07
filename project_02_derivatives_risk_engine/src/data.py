import pandas as pd
import numpy as np
import yfinance as yf

def get_nearest_expiration(
        ticker_symbol: str,
        target_days: int,
        valuation_date: pd.Timestamp | None = None
) -> pd.Timestamp:
    """
    Get the nearest option expiration date based on target days.

    Parameters
    ----------
    ticker_symbol : str
        Yahoo Finance ticker symbol.
    target_days : int
        Target number of days to expiration.
    valuation_date : pd.Timestamp, optional
        Date used for calculations. Defaults to today's date.

    Returns
    -------
    pd.Timestamp
        Nearest expiration date.
    """
    if valuation_date is None:
        valuation_date = pd.Timestamp.today().normalize()

    ticker = yf.Ticker(ticker_symbol)

    expirations = pd.to_datetime(ticker.options)

    days_to_expiry = (expirations - valuation_date).days

    nearest_expiry_index = np.argmin(np.abs(days_to_expiry - target_days))

    return expirations[nearest_expiry_index]


def get_option_chain_data(
        ticker_symbol: str,
        target_days: int,
        valuation_date: pd.Timestamp | None = None,
        clean: bool = True
) ->pd.DataFrame:
    """
    Retrieve, standardize, and optionally clean an option chain.

    Parameters
    ----------
    ticker_symbol : str
        Yahoo Finance ticker symbol.

    target_days : int
        Target number of days to expiration.

    valuation_date : pd.Timestamp, optional
        Date used for calculating time to expiration.
        Defaults to today's date.

    clean : bool, default=True
        If True, remove contracts with invalid quotes and restrict
        the dataset to options with moneyness between 0.80 and 1.20.

    Returns
    -------
    pd.DataFrame
        Standardized option-chain dataset containing calls and puts.
    """

    if valuation_date is None:
        valuation_date = pd.Timestamp.today().normalize()

    ticker = yf.Ticker(ticker_symbol)

    spot = ticker.history(period="1d")["Close"].iloc[-1]

    expiration = get_nearest_expiration(ticker_symbol, target_days, valuation_date)

    option_chain = ticker.option_chain(expiration.strftime("%Y-%m-%d"))

    calls = option_chain.calls.copy()
    puts = option_chain.puts.copy()

    calls['option_type'] = 'call'
    puts['option_type'] = 'put'

    calls['expiration'] = expiration
    puts['expiration'] = expiration

    options = pd.concat([calls, puts], ignore_index=True)
    options['spot'] = spot

    options = options.rename(
        columns={
            "contractSymbol": "contract_symbol",
            "lastPrice": "last_price",
            "openInterest": "open_interest",
            "impliedVolatility": "implied_volatility",
            "inTheMoney": "in_the_money"
        }
    )

    options['days_to_expiry'] = (expiration - valuation_date).days

    options['T'] = options['days_to_expiry'] / 365

    options['mid_price'] = (options['ask'] + options['bid']) / 2

    options['moneyness'] = options['strike'] / options['spot']

    options['intrinsic_value'] = np.where(
        options['option_type'] == 'call', 
        np.maximum(0, options['spot'] - options['strike']), 
        np.maximum(0, options['strike'] - options['spot'])
    )

    options['time_value'] = options['mid_price'] - options['intrinsic_value']

    if clean:
        options = options[
            (options['bid'] > 0) & 
            (options['ask'] > 0) & 
            (options['ask'] > options['bid']) & 
            (options['moneyness'] >= 0.80) & 
            (options['moneyness'] <= 1.20)].copy()

    
    return options.reset_index(drop=True)
