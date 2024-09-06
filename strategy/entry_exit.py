import MetaTrader5 as mt5
from indicators.support_resistance import calculate_support_resistance
from strategy.market_structure import get_market_structure
from data.historical_data import load_data

def check_entry_conditions(symbol, timeframe):
    try:
        market_structure = get_market_structure(timeframe)
        # Load data and calculate support/resistance
        data = load_data(f'data/{timeframe}_data.csv')
        support, resistance = calculate_support_resistance(data)
        
        # Example entry logic
        latest_price = data['close'].iloc[-1]
        if market_structure == 'bullish' and latest_price > resistance:
            return 'buy'
        elif market_structure == 'bearish' and latest_price < support:
            return 'sell'
    except Exception as e:
        log_message(f"Error checking entry conditions for {symbol}: {str(e)}")
    return None
