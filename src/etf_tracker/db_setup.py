from sqlalchemy import text
from src.etf_tracker.database import engine
from dotenv import load_dotenv
import os

load_dotenv()

def init_db(table_name=os.getenv("TABLE_NAME")):
    query = text(f"""
                 CREATE TABLE IF NOT EXISTS {table_name}(
                     id SERIAL PRIMARY KEY,
                     symbol TEXT NOT NULL,
                     price_close REAL NOT NULL,
                     price_open REAL,
                     price_high REAL,
                     price_low REAL,
                     volume BIGINT,
                     timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                 );
                 """)

    try:
        with engine.connect() as conn:
            conn.execute(query)
            conn.commit()
            print("Table is ready.")
    except Exception as e:
        print(e)
    if __name__ == "__main__":
        init_db()