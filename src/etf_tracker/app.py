import streamlit as st
import plotly.express as px
from database import load_from_db
from dotenv import load_dotenv
import os

load_dotenv()

def make_plot(period,ticker: str) -> None:
    df = load_from_db(period,ticker)
    if not df.empty:
        latest_data = df.date.max().strftime("%Y-%m-%d")
        fig = px.line(df, x="date", y="price_close", title=f"Price History for {ticker}<br>Latest data from {latest_data}")
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Could not find any data for this ticker.")


st.title("My ETF Tracker")

tickers_list = os.getenv("tickers").split(",")

ticker = st.radio(
    "Choose one of the following ETFs",
    tickers_list
)

periods = ["1d", "1w", "1mo", "3mo", "1y", "5y"]

time_range = st.segmented_control(
    "Select Timeframe",
    options=periods,
    default="1d"
)

if time_range=="1d":
    if ticker:
        make_plot("1d",ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")
if time_range=="1w":
    if ticker:
        make_plot("1w",ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")
if time_range=="1mo":
    if ticker:
        make_plot("1mo", ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")
if time_range=="3mo":
    if ticker:
        make_plot("3mo", ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")
if time_range=="1y":
    if ticker:
        make_plot("1y", ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")
if time_range=="5y":
    if ticker:
        make_plot("5y", ticker)
    else:
        st.info("Please enter a ticker symbol to view the performance graph.")






