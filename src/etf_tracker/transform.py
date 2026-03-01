import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def transform_data(df: DataFrame, ticker: str) -> DataFrame:
    """
    Transforms the raw JSON data into a list of dictionaries.

    Args:
        data: A dictionary the response from the CoinGecko API as a dictionary.

    Returns:
        A list of dictionaries containing the same data but in a specific format.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    df.columns = [col.lower() for col in df.columns]

    df.rename(columns={
        'high': 'price_high',
        'low': 'price_low',
        'open': 'price_open',
        'close': 'price_close',
    }, inplace=True)

    df["symbol"] = ticker

    return df




