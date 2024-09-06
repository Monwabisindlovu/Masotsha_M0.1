import pandas as pd
from utils import log_message

def load_data(file_path):
    """Load historical data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        log_message(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def preprocess_data(data):
    """Preprocess data for analysis."""
    try:
        # Example preprocessing: filling missing values
        data = data.ffill()
        return data
    except Exception as e:
        log_message(f"Error preprocessing data: {str(e)}")
        return data

def calculate_moving_average(data, period=50):
    """Calculate moving average."""
    try:
        return data.rolling(window=period).mean()
    except Exception as e:
        log_message(f"Error calculating moving average: {str(e)}")
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
        log_message(f"Error getting market structure: {str(e)}")
        return None
