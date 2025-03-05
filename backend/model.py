import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model, load_model
from keras.layers import LSTM, Dense, Dropout, BatchNormalization, Input, AdditiveAttention, Multiply, Flatten, Reshape
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress INFO and WARNING logs


# Function to preprocess stock data for LSTM model
def preprocess_data(data):
    closing_prices = data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(closing_prices)

    X = [scaled_data[i-60:i, 0] for i in range(60, len(scaled_data))]
    X = np.array(X).reshape(len(X), 60, 1)

    return X, scaler

# Function to create the LSTM model
def create_model(input_shape):
    print("ENTERED CREATE MODEL FUNCTION")
    input_layer = Input(shape=input_shape)

    lstm_out_1 = LSTM(units=50, return_sequences=True)(input_layer)
    lstm_out_2 = LSTM(units=50, return_sequences=True)(lstm_out_1)
    dropout_layer = Dropout(0.2)(lstm_out_2)
    batch_norm_layer = BatchNormalization()(dropout_layer)

    attention = AdditiveAttention(name='attention_weight')
    attention_result = attention([batch_norm_layer, batch_norm_layer])

    multiply_layer = Multiply()([batch_norm_layer, attention_result])
    reshape_layer = Reshape((-1, 50))(multiply_layer)
    flatten_layer = Flatten()(reshape_layer)
    output_layer = Dense(1)(flatten_layer)

    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer='adam', loss='mean_squared_error')
    print("FINISHED CREATE MODEL FUNCTION")

    return model

# Function to predict next 4 days' stock prices
def predict_stock_prices(model, X, scaler):
    predicted_prices = []
    current_batch = X[-1].reshape(1, 60, 1)

    for _ in range(4):  # Predict 4 days ahead
        next_prediction = model.predict(current_batch)
        current_batch = np.append(current_batch[:, 1:, :], next_prediction.reshape(1, 1, 1), axis=1)
        predicted_prices.append(scaler.inverse_transform(next_prediction)[0, 0])

    return predicted_prices
