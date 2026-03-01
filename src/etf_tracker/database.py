import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

DB_CONFIG = {
    'dbname': os.getenv("DBNAME"),
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': os.getenv("HOST"),
    'port': os.getenv("PORT"),
}


engine = create_engine(database_url)

def init_db():
    with psycopg2.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS etf_prices \
                ( \
                    id \
                    SERIAL \
                    PRIMARY \
                    KEY, \
                    symbol \
                    TEXT \
                    NOT \
                    NULL, \
                    price_close \
                    REAL \
                    NOT \
                    NULL, \
                    price_open \
                    REAL, \
                    price_high \
                    REAL, \
                    price_low \
                    REAL, \
                    volume \
                    BIGINT, \
                    timestamp \
                    TIMESTAMP \
                    WITH \
                    TIME \
                    ZONE \
                    DEFAULT \
                    CURRENT_TIMESTAMP
                ); \
                """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()


def save_to_db(df,table_name=os.getenv("TABLE_NAME")) -> None:
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except psycopg2.Error as e:
        print(e)

def load_from_db(period,etf_symbol,table_name=os.getenv("TABLE_NAME")) -> None:
    date_query = f"""
    SELECT MAX(CAST(date AS TIMESTAMP))
    FROM {table_name}
    """
    date_df = pd.read_sql_query(date_query, con=engine)
    end_date = date_df.iloc[0,0]
    if period == "1d":
        start_date = end_date - relativedelta(days=1)
    elif period == "1w":
        start_date = end_date - relativedelta(weeks=1)
    elif period == "1mo":
        start_date = end_date - relativedelta(months=1)
    elif period == "3mo":
        start_date = end_date - relativedelta(months=3)
    elif period == "1y":
        start_date = end_date - relativedelta(years=1)
    else:
        start_date = end_date - relativedelta(years=5)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    try:
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE symbol = '{etf_symbol}'
        AND date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date ASC;
        """
        df = pd.read_sql_query(query, con=engine)
        return df
    except psycopg2.Error as e:
        print(e)
