import yfinance as yf
from pandas.core.interchange.dataframe_protocol import DataFrame


def fetch_etf_data(input_ticker: str) -> DataFrame:
    """
    Fetches current market prices for specified ETFs from Yfinance.

    Args:
        coin_IDs: A list of coin IDs to fetch (e.g. ['bitcoin', 'ethereum']).

    Returns:
        A dictionary containing the raw JSON response from the API.
    """

    df = yf.download(input_ticker, period="5y", auto_adjust=True)
    return df



