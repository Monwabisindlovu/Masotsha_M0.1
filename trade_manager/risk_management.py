from trade_manager.logger import log_message
import logging

def calculate_take_profit(entry_price, direction, pips=500):
    """Calculate take profit based on entry price and direction (buy/sell)."""
    try:
        if direction == 'buy':
            return entry_price + pips * 0.0001  # Add 500 pips to the entry price for buy
        elif direction == 'sell':
            return entry_price - pips * 0.0001  # Subtract 500 pips for sell
    except Exception as e:
        log_message(f"Error calculating take profit: {str(e)}", level=logging.ERROR)
    return None

def calculate_stop_loss(entry_price, direction, support_resistance, pips=20):
    """Calculate stop loss 20 pips above/below support/resistance levels."""
    try:
        if direction == 'buy':
            return support_resistance - pips * 0.0001  # Stop loss 20 pips below support
        elif direction == 'sell':
            return support_resistance + pips * 0.0001  # Stop loss 20 pips above resistance
    except Exception as e:
        log_message(f"Error calculating stop loss: {str(e)}", level=logging.ERROR)
    return None

def calculate_support_resistance(data):
    """Identify support and resistance levels from historical data."""
    try:
        if data.empty:
            log_message("Data is empty. Cannot calculate support/resistance.", level=logging.ERROR)
            return None, None

        high = data['high'].max()
        low = data['low'].min()
        log_message(f"Calculated support: {low}, resistance: {high}", level=logging.INFO)
        return low, high  # Return support (low) and resistance (high)
    except Exception as e:
        log_message(f"Error calculating support/resistance: {str(e)}", level=logging.ERROR)
        return None, None
