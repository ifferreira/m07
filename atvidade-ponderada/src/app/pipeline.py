import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.metrics import mean_squared_error
import yfinance as yf
import math
import os

def fetch_crypto_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Close'].values

def scale_data(data):
    scaler = MinMaxScaler()
    return scaler, scaler.fit_transform(data.reshape(-1, 1))

def create_dataset(dataset, time_step):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(input_shape, 1)))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def train_lstm_model(model, X_train, Y_train, epochs=100, batch_size=64):
    model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model

def predict_lstm(model, X):
    return model.predict(X)

def inverse_scale(scaler, data):
    return scaler.inverse_transform(data.reshape(1, -1))

def calculate_rmse(Y_true, Y_pred):
    return math.sqrt(mean_squared_error(Y_true, Y_pred))

def predict_next_days(model, data, time_step, days_to_predict=7):
    temp_input = data[-time_step:].flatten().tolist()
    predictions = []
    for _ in range(days_to_predict):
        x_input = np.array(temp_input[-time_step:]).reshape(1, time_step, 1)
        pred = model.predict(x_input, verbose=0)
        predictions.append(pred[0][0])
        temp_input.append(pred[0][0])
    return np.array(predictions)

def buy_sell_decision(predictions):
    start_price = predictions[0][0]
    end_price = predictions[0][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    if end_price > start_price:
        return f"Compre: o preço está previsto para subir {percentage_change:.2f}%."
    else:
        return f"Venda: o preço está previsto para cair {abs(percentage_change):.2f}%."
    
def retrain_model(start_date, end_date):
    data = fetch_crypto_data('BTC-USD', start_date, end_date)
    scaler, data_scaled = scale_data(data)

    train_size = int(len(data_scaled) * 0.65)
    train_data = data_scaled[:train_size]

    time_step = 100
    X_train, Y_train = create_dataset(train_data, time_step)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

    model = build_lstm_model(time_step)
    trained_model = train_lstm_model(model, X_train, Y_train)

    model_save_path = os.path.join(os.path.dirname(__file__), 'new_model.h5')
    trained_model.save(model_save_path)

def main_pipeline(start_date, end_date):
    data = fetch_crypto_data('BTC-USD', start_date, end_date)
    scaler, data_scaled = scale_data(data)
    
    train_size = int(len(data_scaled) * 0.65)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]
    
    time_step = 100
    X_train, Y_train = create_dataset(train_data, time_step)
    X_test, Y_test = create_dataset(test_data, time_step)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    model = build_lstm_model(time_step)
    trained_model = train_lstm_model(model, X_train, Y_train, X_test, Y_test)

    test_predictions = predict_lstm(trained_model, X_test)
    test_predictions_inverse = inverse_scale(scaler, test_predictions)
    Y_test_inverse = inverse_scale(scaler, Y_test.reshape(-1, 1))

    rmse = calculate_rmse(Y_test_inverse, test_predictions_inverse)
    print(f"Test RMSE: {rmse}")

    future_predictions = predict_next_days(trained_model, test_data, time_step, days_to_predict=7)
    future_predictions_inverse = inverse_scale(scaler, future_predictions)

    decision = buy_sell_decision(future_predictions_inverse)
    print(decision)

