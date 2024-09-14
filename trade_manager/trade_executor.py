import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import logging
import MetaTrader5 as mt5
from trade_manager.logger import log_message
from trade_manager.risk_management import calculate_take_profit, calculate_stop_loss, calculate_support_resistance
from data.historical_data import load_data, preprocess_data
from config.credentials import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
import os
import pandas as pd
import time

# Path to MetaTrader 5 executable
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_config(file_path):
    """Load configuration from a JSON file."""
    abs_path = os.path.abspath(file_path)
    log_message(f"Loading config from: {abs_path}")
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        log_message(f"Config file not found: {file_path}", level=logging.ERROR)
        return None
    except json.JSONDecodeError:
        log_message(f"Invalid JSON format in config file: {file_path}", level=logging.ERROR)
        return None

def initialize_mt5():
    """Initialize the MetaTrader 5 connection."""
    log_message(f"Initializing MetaTrader 5 from path: {MT5_PATH}")

    # Attempt to initialize MetaTrader 5 with specified path
    if not mt5.initialize(path=MT5_PATH):
        log_message(f"Failed to initialize MetaTrader 5, error code: {mt5.last_error()}", level=logging.ERROR)
        return False

    # Log in to the account
    login_status = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    if not login_status:
        log_message(f"Failed to login to account {MT5_LOGIN}, error code: {mt5.last_error()}", level=logging.ERROR)
        mt5.shutdown()
        return False

    log_message(f"Logged in to account {MT5_LOGIN} successfully.")
    return True

def place_order(symbol, action, lot_size, stop_loss, take_profit):
    """Place an order with given parameters."""
    try:
        order_type = mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            log_message(f"Symbol {symbol} info is not available.", level=logging.ERROR)
            return None

        if not symbol_info.visible:
            log_message(f"Symbol {symbol} is not visible.", level=logging.ERROR)
            if not mt5.symbol_select(symbol, True):
                log_message(f"Failed to select symbol {symbol}.", level=logging.ERROR)
                return None

        price = mt5.symbol_info_tick(symbol).ask if action == 'buy' else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "deviation": 20,
            "magic": 123456,
            "comment": "Masotsha_M0.1",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            log_message(f"Failed to place order for {symbol}, error: {result.retcode}", level=logging.ERROR)
        else:
            log_message(f"Order placed successfully for {symbol}, result: {result}")
        return result

    except Exception as e:
        log_message(f"Error placing order for {symbol}: {str(e)}", level=logging.ERROR)
        return None

def calculate_stop_loss_and_take_profit(symbol, action):
    """Calculate stop loss and take profit levels based on fixed pip values."""
    try:
        # Get the current price
        symbol_info_tick = mt5.symbol_info_tick(symbol)
        if symbol_info_tick is None:
            log_message(f"Symbol {symbol} info not available.", level=logging.ERROR)
            return None, None

        price = symbol_info_tick.ask if action == 'buy' else symbol_info_tick.bid

        # Convert pip values to price difference based on symbol's tick size
        pip_size = mt5.symbol_info(symbol).point  # This gives the size of 1 pip for the symbol

        stop_loss_pips = 10  # 10 pips for stop loss
        take_profit_pips = 30  # 30 pips for take profit

        if action == 'buy':
            stop_loss = price - (stop_loss_pips * pip_size)  # For buy, stop loss is below the price
            take_profit = price + (take_profit_pips * pip_size)  # Take profit is above the price
        else:
            stop_loss = price + (stop_loss_pips * pip_size)  # For sell, stop loss is above the price
            take_profit = price - (take_profit_pips * pip_size)  # Take profit is below the price

        return stop_loss, take_profit

    except Exception as e:
        log_message(f"Error calculating stop loss and take profit for {symbol}: {str(e)}", level=logging.ERROR)
        return None, None
    
def load_data(file_path):
    """Load historical data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        if 'time' not in data.columns:
            log_message(f"'time' column not found in data.", level=logging.ERROR)
            return None
        return data
    except FileNotFoundError:
        log_message(f"File not found: {file_path}", level=logging.ERROR)
        return None
    except pd.errors.EmptyDataError:
        log_message(f"Data is empty. Cannot calculate support/resistance.", level=logging.ERROR)
        return None

def main():
    """Main execution function."""
    # Load configuration
    config = load_config('../config/config.json')  # Adjust path to config
    if not config:
        return

    # Access configuration parameters
    lot_size = config.get('LOT_SIZE')
    max_trades_per_day = config.get('MAX_TRADES_PER_DAY')
    max_positions_per_trade = config.get('MAX_POSITIONS_PER_TRADE')
    trading_pairs = config.get('TRADING_PAIRS')

    # Ensure trading_pairs is a list and add XAUUSD if not already present
    if trading_pairs is None:
        trading_pairs = ['XAUUSD']
    elif 'XAUUSD' not in trading_pairs:
        trading_pairs.append('XAUUSD')

    if not initialize_mt5():
        return

    trades_taken = 0

    for symbol in trading_pairs:
        if trades_taken >= max_trades_per_day:
            break

        action = 'buy'  # Example action
        stop_loss, take_profit = calculate_stop_loss_and_take_profit(symbol, action)
        if stop_loss and take_profit:
            for _ in range(max_positions_per_trade):
                result = place_order(symbol, action, lot_size, stop_loss, take_profit)
                if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                    trades_taken += 1
                    if trades_taken >= max_trades_per_day:
                        break
                time.sleep(1)  # Small delay between orders

if __name__ == "__main__":
    main()
