import streamlit as st
from backend.data_fetcher import *
from backend.top_buy import *

# Set page configuration (optional)
st.set_page_config(page_title="Stock Dashboard", page_icon="📈", layout="wide")

# Title of the app
st.title("Welcome to the S&P 500 Stock Analysis 📊")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home"])

# Define page content
if page == "Home":

    st.subheader("Search for a stock to start your analysis")
    st.write("Accurate information including all the companies in the S&P500 index. See stock prices, news, financials, forecasts, charts and more.")
    tickers = fetch_sp500_tickers()

    # Search Bar with Scrollable List
    selected_stock = st.selectbox(
        "🔍 Search for a stock:", 
        tickers,  # List of stocks
        index=None,  # No default selection
        help="Start typing to search or scroll through the list"
    )

    if st.button("Top Rated Stocks"):
        get_top_strong_buy_yfinance()
 

    # If a stock is selected, redirect to the details page
    if selected_stock:
        st.session_state["selected_stock"] = selected_stock
        st.switch_page("pages/stock_details.py")  

