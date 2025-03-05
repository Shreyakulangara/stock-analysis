import streamlit as st
import yfinance as yf
from backend.data_fetcher import fetch_data, fetch_news
from backend.model import preprocess_data, predict_stock_prices, create_model
from backend.visualization import display_predictions, plot_stock_prices
from keras.models import load_model

st.set_page_config(page_title="Stock Details", page_icon="📊")

if "selected_stock" in st.session_state:
    ticker = st.session_state["selected_stock"]
    st.title(f"📊 {ticker} Stock Details")

    company = yf.Ticker(ticker)
    company_name = company.info.get('longName', 'Name not available')
    st.subheader(company_name)


    # Fetch historical stock data
    data = fetch_data(ticker)

        # Display stock price chart
    # st.subheader("📈 Stock Price Chart")
    # st.line_chart(data["Close"])  # Show closing prices

    # Preprocess data for prediction
    X, scaler = preprocess_data(data)

    # Load or train the model
    try:
        model = load_model(f"{ticker}_model.h5")
    except:
        st.warning("No saved model found. Training a new one...")
        model = create_model((X.shape[1], 1))
        model.fit(X, X, epochs=10, batch_size=32)
        model.save(f"{ticker}_model.h5")

    predicted_prices = predict_stock_prices(model, X, scaler)

    st.subheader("🔮 Predicted Prices")
    display_predictions(predicted_prices)
    plot_stock_prices(data, predicted_prices)

        # Show latest news
    st.subheader("📰 Latest News")
    news = fetch_news(ticker)
    for article in news:
        print("article",article)
        st.markdown(f"### [{article['title']}]({article['url']})")
else:
    st.error("No stock selected. Go back to the Home page.")