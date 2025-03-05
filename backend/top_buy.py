import streamlit as st
import yfinance as yf
import pandas as pd
from backend.data_fetcher import fetch_sp500_tickers

def get_top_strong_buy_yfinance(top_n=50):
    """Retrieves the top N stocks with the strongest buy recommendations."""
       
    sp500_tickers = fetch_sp500_tickers()

    # Use yfinance to fetch data in bulk
    stocks = yf.Tickers(" ".join(sp500_tickers))  # Batch request all tickers
    print("stocks",stocks)
    # Extract recommendations
    recommendations = []
    for ticker in sp500_tickers:
        try:
            stock = stocks.tickers[ticker]
            info = stock.info
            recommendation = info.get("recommendationKey", "N/A")
            
            if recommendation == "strong_buy":
                recommendations.append([
                    info.get("longName", ticker),  # Company Name
                    ticker,  
                    info.get("recommendationMean", "N/A"),
                    recommendation,
                    info.get("targetMeanPrice", "N/A"),
                    info.get("marketCap", "N/A"),
                    info.get("industry", "N/A"),
                    info.get("currentPrice", "N/A"),
                    info.get("regularMarketChangePercent", "N/A")
                ])               
        
        except Exception as e:
            continue
    print("recommendations",recommendations)


    # Convert to DataFrame
    columns = ["Company Name", "Ticker", "Recommendation Mean", "Recommendation Key", 
            "Target Mean Price", "Market Cap", "Industry", "Current Price", "% Change (Day)"]

    df = pd.DataFrame(recommendations, columns=columns)

    # Display Top 50 Strong Buy Stocks
    st.dataframe(df.head(50))  # Display as interactive table

    # Button to refresh data
    if st.button("🔄 Refresh Data"):
        st.rerun()