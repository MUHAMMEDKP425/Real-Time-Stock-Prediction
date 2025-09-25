import streamlit as st
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
import time

# --- Load the saved model, scaler, and the full dataset ---
try:
    model = load_model('stock_prediction_model.h5')
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    df = pd.read_csv('NIFTY50_all.csv')
except Exception as e:
    st.error(f"Error loading files. Make sure all files are in the same folder. Error: {e}")
    st.stop()


# --- Streamlit App Setup ---
st.set_page_config(layout="wide")
st.title("Real-Time Stock Price Prediction Dashboard")
placeholder = st.empty()


# --- Data Preparation for Simulation ---
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# Let's simulate with one stock, for example, 'TCS'
df_stock = df[df['Symbol'] == 'TCS'].copy()

# Get the last 60 days to start our prediction sequence
initial_sequence_data = df_stock['Close'].values[-100:-40]
last_60_days = list(scaler.transform(initial_sequence_data.reshape(-1, 1)))

# The rest of the data will be our "live" stream
live_stream_data = df_stock['Close'].values[-40:]

# Dataframe to store the visual history
history_df = pd.DataFrame(columns=['Actual Price', 'Predicted Price'])


# --- Live Dashboard Loop ---
for actual_price in live_stream_data:
    
    # --- Prediction Logic ---
    sequence_for_prediction = np.array([last_60_days])
    
    predicted_scaled_price = model.predict(sequence_for_prediction, verbose=0)
    predicted_price = scaler.inverse_transform(predicted_scaled_price)[0][0]
    
    # --- Update Dashboard ---
    new_data = pd.DataFrame({'Actual Price': [actual_price], 'Predicted Price': [predicted_price]})
    history_df = pd.concat([history_df, new_data], ignore_index=True)
    
    if len(history_df) > 50:
        history_df = history_df.tail(50)

    with placeholder.container():
        st.header("Live Price Updates (Simulated)")
        
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Last Actual Price 🟢", value=f"₹{actual_price:.2f}")
        kpi2.metric(label="Next Day Prediction 🔮", value=f"₹{predicted_price:.2f}")
        
        st.header("Prediction vs. Actual Price")
        st.line_chart(history_df)

    # --- Update the sequence for the next loop ---
    scaled_new_price = scaler.transform([[actual_price]])
    last_60_days.append(scaled_new_price[0])
    last_60_days = last_60_days[1:]
    
    time.sleep(1) # Pause for 1 second to simulate real-time