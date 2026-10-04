import pandas as pd
import yfinance as yf

def download_prices(
    tickers: list[str],
    start: str,
    end: str
) -> pd.DataFrame:
    
    """Function to download prices of tickers.
    Tickers - A list of tickers. eg ["MSFT", "APQL"]
    start - start date in the format YYYY-MM-DD
    end - end date in the same format
    """
    
    data = yf.download(
        tickers=tickers, 
        start=start, 
        end=end)
    
    if data.empty:
        raise ValueError("No data was returned")
    
    prices = data['Close'].copy()
    
    return prices