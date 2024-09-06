import pandas as pd
from utils.logger import log_message  # Ensure you have this import for logging

def calculate_moving_average(data, period):
    try:
        return data.rolling(window=period).mean()
    except Exception as e:
        log_message(f"Error calculating moving average: {str(e)}")
        return None

def calculate_rsi(data, period=14):
    try:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    except Exception as e:
        log_message(f"Error calculating RSI: {str(e)}")
        return None
