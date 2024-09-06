import pandas as pd

def calculate_support_resistance(data):
    try:
        high = data['high'].max()
        low = data['low'].min()
        return high, low
    except Exception as e:
        log_message(f"Error calculating support/resistance: {str(e)}")
        return None, None
