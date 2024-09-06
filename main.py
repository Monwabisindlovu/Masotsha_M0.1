# Masotsha_M0.1/main.py
from trade_manager.trade_executor import execute_trade
from trade_manager.logger import setup_logger, log_message  # Import logger
from data.historical_data import load_data
from strategy.market_structure import get_market_structure
import MetaTrader5 as mt5
import datetime
import time

def main():
    setup_logger()  # Initialize logging at the start

    global trade_count, last_trade_date
    config = load_config()

    if not mt5.initialize():
        log_message(f"MetaTrader5 initialization failed, error code: {mt5.last_error()}", logging.ERROR)
        return

    log_message("MetaTrader5 initialized successfully")
    
    while True:
        current_date = datetime.datetime.now().date()
        if current_date != last_trade_date:
            trade_count = 0
            last_trade_date = current_date

        if trade_count < config['MAX_TRADES_PER_DAY']:
            for symbol in config['TRADING_PAIRS']:
                log_message(f"Checking entry conditions for {symbol}")
                
                market_structure = get_market_structure(symbol, 'H4')
                if market_structure:
                    log_message(f"Market structure for {symbol}: {market_structure}")
                    action = 'buy' if market_structure == 'bullish' else 'sell'

                    result = execute_trade(symbol, action, config['LOT_SIZE'], 'H4')
                    log_message(f"Trade result for {symbol}: {result}")
                    trade_count += 1

        time.sleep(60)