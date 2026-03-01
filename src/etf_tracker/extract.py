import yfinance as yf
from pandas.core.interchange.dataframe_protocol import DataFrame


def fetch_etf_data(input_ticker: str) -> DataFrame:
    df = yf.download(input_ticker, period="5y", auto_adjust=True)
    return df



