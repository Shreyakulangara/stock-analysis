from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data_fetcher import fetch_sp500_tickers, fetch_data, fetch_news
from model import create_model, preprocess_data, predict_stock_prices
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)

# Load S&P 500 tickers
@app.get("/tickers")
def get_tickers():
    return {"tickers": fetch_sp500_tickers()}

# Get stock historical data
@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        print(" From get_stock_data: TICKER NAME", ticker)
        print(ticker)
        logger.info(f"Request received for ticker: {ticker}")

        data = fetch_data(ticker)
        print("FETCHED DATA", len(data))
        return data.tail(100).to_dict(orient="records")  # Send last 100 records
    except Exception as e:
        logger.error(f"Error processing request for {ticker}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Get latest stock news
@app.get("/news/{ticker}")
def get_stock_news(ticker: str):
    return {"news": fetch_news(ticker)}

# Predict stock prices
@app.get("/predict/{ticker}")
def predict_stock(ticker: str):
    try:
        data = fetch_data(ticker)
        X, scaler = preprocess_data(data)
        model = create_model((60, 1))
        predictions = predict_stock_prices(model, X, scaler)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
