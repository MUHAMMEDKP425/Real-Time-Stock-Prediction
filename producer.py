import pandas as pd
from kafka import KafkaProducer
import json
import time

# --- Load the dataset ---
try:
    df = pd.read_csv('NIFTY50_all.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    # Filter for just one stock to stream
    df_stock = df[df['Symbol'] == 'TCS'].copy()
except FileNotFoundError:
    print("Error: NIFTY50_all.csv not found. Make sure it's in the same folder.")
    exit()

# --- Kafka Producer Setup ---
try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print(f"Could not connect to Kafka. Please ensure Kafka is running. Error: {e}")
    exit()


print("Producer is starting to send data...")

# --- Send data to the 'stock-topic' ---
# We use .head(50) to only send the first 50 prices for a quick test
for index, row in df_stock.head(50).iterrows():
    message = row.to_dict()
    # Convert Timestamp to string for JSON
    message['Date'] = message['Date'].strftime('%Y-%m-%d')
    producer.send('stock-topic', value=message)
    print(f"Sent: {message['Symbol']} price {message['Close']}")
    time.sleep(1) # Pause for 1 second

print("\n--- Producer has finished sending 50 messages. ---")