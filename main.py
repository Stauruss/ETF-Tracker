import time
import pandas as pd
from src.etf_tracker.extract import fetch_etf_data
from src.etf_tracker.transform import transform_data
from src.etf_tracker.database import save_to_db
from src.etf_tracker.db_setup import init_db
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # 1. Initialize
    init_db()

    while True:
        tickers = os.getenv("tickers").split(",")
        clean_data = pd.DataFrame()

        for ticker in tickers:
            raw_data = fetch_etf_data(ticker)
            temp_df = transform_data(raw_data, ticker)
            frames = [clean_data, temp_df]
            clean_data = pd.concat(frames)

        save_to_db(clean_data)
        print("Database updated!")
        time.sleep(60)

if __name__ == "__main__":
    main()