import pandas as pd
from trade_manager.logger import log_message
import logging

def load_data(file_path):
    """Load historical data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        # Check if the DataFrame is empty and log a warning
        if data.empty:
            log_message(f"Loaded data from {file_path} is empty.", level=logging.WARNING)
        else:
            log_message(f"Data loaded successfully from {file_path}")
        return data
    except FileNotFoundError:
        # Log if file is not found
        log_message(f"File not found: {file_path}", level=logging.ERROR)
        return pd.DataFrame()  # Return an empty DataFrame on error
    except pd.errors.EmptyDataError:
        # Log if file is empty or corrupted
        log_message(f"Empty data file: {file_path}", level=logging.ERROR)
        return pd.DataFrame()
    except Exception as e:
        # Log any other exceptions that occur
        log_message(f"Error loading data from {file_path}: {str(e)}", level=logging.ERROR)
        return pd.DataFrame()

def preprocess_data(data):
    """Preprocess data for analysis."""
    try:
        # Ensure 'time' column is in datetime format
        if 'time' in data.columns:
            data['time'] = pd.to_datetime(data['time'])
        else:
            log_message(f"'time' column not found in data.", level=logging.ERROR)
            return pd.DataFrame()  # Return an empty DataFrame if 'time' column is missing

        # Drop rows with NaN values
        data = data.dropna()
        return data
    except Exception as e:
        log_message(f"Error preprocessing data: {str(e)}", level=logging.ERROR)
        return data

def calculate_moving_average(data, period=50):
    """Calculate moving average."""
    try:
        return data['close'].rolling(window=period).mean()
    except Exception as e:
        log_message(f"Error calculating moving average: {str(e)}", level=logging.ERROR)
        return pd.Series()

def get_market_structure(symbol, timeframe):
    """Determine market structure based on historical data and moving average."""
    try:
        data = load_data(f'data/{symbol}_{timeframe}_data.csv')
        data = preprocess_data(data)
        moving_avg = calculate_moving_average(data['close'], period=50)
        latest_price = data['close'].iloc[-1]
        
        if latest_price > moving_avg.iloc[-1]:
            return 'bullish'
        else:
            return 'bearish'
    except Exception as e:
        log_message(f"Error getting market structure: {str(e)}", level=logging.ERROR)
        return None
