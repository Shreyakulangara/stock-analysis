import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Function to display stock predictions
def display_predictions(predicted_prices):
    prediction_dates = pd.date_range(start=pd.Timestamp.today(), periods=4, freq='D')
    predictions_df = pd.DataFrame({'Date': prediction_dates.strftime('%Y-%m-%d'),
                                   'Predicted Price (USD)': [round(price, 2) for price in predicted_prices]})
    # st.write("### 📆 Prediction Table")
    st.dataframe(predictions_df)

    st.write("### 📈 Key Metrics")
    for i, price in enumerate(predicted_prices):
        delta = 0 if i == 0 else price - predicted_prices[i - 1]
        st.metric(label=f"📅 {predictions_df['Date'][i]}", value=f"${price:.2f}", delta=f"{delta:.2f} USD")

# # Function to plot actual vs predicted stock prices
# def plot_stock_prices(data, predicted_prices):
#     prediction_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=4)
#     predictions_df = pd.DataFrame(predicted_prices, index=prediction_dates, columns=['Predicted Close'])

#     plt.figure(figsize=(12, 6))
#     plt.plot(data.index, data['Close'], label="Actual Prices", color='blue')
#     plt.plot(predictions_df.index, predictions_df['Predicted Close'], label="Predicted Prices", color='red', linestyle='--', marker='o')
#     plt.xlabel("Date")
#     plt.ylabel("Stock Price (USD)")
#     plt.title("Stock Prices: Actual vs Predicted (Next 4 Days)")
#     plt.legend()
#     st.pyplot(plt)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to plot stock prices (with beautiful styling)
def plot_stock_prices(data, predicted_prices):
    # Ensure seaborn styles are applied
    sns.set_style("darkgrid")  

    # Generate future dates for predictions
    prediction_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=len(predicted_prices))
    predictions_df = pd.DataFrame(predicted_prices, index=prediction_dates, columns=['Predicted Close'])

    # Use a valid Matplotlib style
    plt.style.use("ggplot")  # Alternative: 'bmh', 'fast', 'seaborn-dark'

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot actual prices
    ax.plot(data.index, data['Close'], label="📈 Actual Prices", color='royalblue', linewidth=2.5)

    # Plot predicted prices with a dashed red line and markers
    ax.plot(predictions_df.index, predictions_df['Predicted Close'], 
            label="🔴 Predicted Prices", color='crimson', linestyle='dashed', marker='o', markersize=8, linewidth=2)

    # Add a shaded area for the prediction period
    ax.axvspan(prediction_dates[0], prediction_dates[-1], color='red', alpha=0.1, label="🔍 Prediction Zone")

    # Improve readability
    ax.set_xlabel("Date", fontsize=14, fontweight='bold')
    ax.set_ylabel("Stock Price (USD)", fontsize=14, fontweight='bold')
    ax.set_title("📊 Stock Prices: Actual vs Predicted (Next 4 Days)", fontsize=16, fontweight='bold')

    # Customize legend
    ax.legend(fontsize=12, loc='upper left', frameon=True, shadow=True)

    # Grid and layout improvements
    ax.grid(True, linestyle='--', alpha=0.6)

    # Display plot in Streamlit
    st.pyplot(fig)


