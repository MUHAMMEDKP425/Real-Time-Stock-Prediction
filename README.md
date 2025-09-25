# Real-Time Stock Price Prediction with LSTM

This project builds an end-to-end pipeline to predict stock prices in real-time. It uses an LSTM deep learning model to make predictions and a Streamlit dashboard to visualize the results.

## Features
- **Data Cleaning:** Prepares the NIFTY 50 dataset for time series forecasting.
- **LSTM Model:** A trained Keras/TensorFlow model that predicts the next day's closing price based on the last 60 days.
- **Real-Time Simulation:** A Streamlit dashboard that simulates a live data feed and updates predictions every second.

## Results
Here is a plot showing the model's predictions versus the actual stock prices from the test set.

*(You should add the screenshot of your matplotlib plot here!)*

## How to Run This Project

1.  **Download the Data:**
    * The `NIFTY50_all.csv` dataset is too large for GitHub. You can download it from Kaggle at this link:
    * [https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data](https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data)
    * Place the `NIFTY50_all.csv` file in this project folder.

2.  **Install the Libraries:**
    * Open your terminal and run:
    ```bash
    pip install streamlit tensorflow scikit-learn pandas numpy
    ```

3.  **Run the Dashboard:**
    * Navigate to the project folder in your terminal and run the following command:
    ```bash
    streamlit run dashboard.py
    ```
