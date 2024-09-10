import logging
from trade_manager.logger import log_message

def format_pips(price, pips):
    """Format the price by adding/subtracting pips."""
    try:
        return price + pips * 0.0001
    except Exception as e:
        log_message(f"Error formatting pips: {str(e)}", level=logging.ERROR)
        return price
