import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch S&P 500 tickers
def fetch_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve S&P 500 tickers from Wikipedia.")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'class': 'wikitable'})

    tickers = []
    for row in table.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if cols:
            ticker = cols[0].text.strip().replace(".", "-")  # Adjust for Yahoo Finance
            tickers.append(ticker)
    print(tickers)
    return tickers

# Function to fetch the latest stock data for a given ticker
def fetch_latest_data(ticker):
    try:
        # Fetch the most recent trading day's data
        data = yf.download(ticker, period="2d", interval="1d", auto_adjust=True)

        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        # Get the last available row
        latest_data = data.iloc[-1]

        # Format the result as a dictionary
        result = {
            "Ticker": ticker,
            "Date": latest_data.name.strftime('%Y-%m-%d'),
            "Open": round(latest_data["Open"], 2),
            "Close": round(latest_data["Close"], 2),
            "High": round(latest_data["High"], 2),
            "Low": round(latest_data["Low"], 2),
            "Volume": int(latest_data["Volume"]),
        }
        print("RESULT")
        print(result)
        return result
    
    except Exception as e:
        raise ValueError(f"Error fetching data for {ticker}: {e}")


# Function to fetch stock historical data
def fetch_data(ticker, start="2001-01-01", interval="1d"):
    try:
        end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        data = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True)
        
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        return data  # Returns as Pandas DataFrame
    
    except Exception as e:
        raise ValueError(f"Error fetching data for {ticker}: {e}")


# Function to fetch latest stock news
def fetch_news(ticker):
    api_key = "0403d223f3624b739ae341c062daacea"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])[:5]  # Return top 5 news articles
    return []
