import MetaTrader5 as mt5
from indicators.support_resistance import calculate_support_resistance
from strategy.market_structure import get_market_structure
from data.historical_data import load_data, preprocess_data
from trade_manager.logger import log_message
import logging

def check_entry_conditions(symbol, timeframe):
    try:
        # Get market structure for the given timeframe
        market_structure = get_market_structure(timeframe)
        
        # Load and preprocess data
        data = load_data(f'data/{symbol}_{timeframe}_data.csv')
        data = preprocess_data(data)
        
        # Calculate support and resistance levels
        support, resistance = calculate_support_resistance(data)
        
        # Example entry logic
        latest_price = data['close'].iloc[-1]
        if market_structure == 'bullish' and latest_price > resistance:
            return 'buy'
        elif market_structure == 'bearish' and latest_price < support:
            return 'sell'
    except Exception as e:
        log_message(f"Error checking entry conditions for {symbol}: {str(e)}", level=logging.ERROR)
    return None
