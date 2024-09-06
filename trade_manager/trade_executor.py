import json
import logging
import MetaTrader5 as mt5
from trade_manager.logger import log_message
from trade_manager.risk_management import calculate_take_profit, calculate_stop_loss, calculate_support_resistance
from data.historical_data import load_data, preprocess_data
from config import credentials
import os

# Path to MetaTrader 5 executable
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

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
    login_status = mt5.login(credentials.MT5_LOGIN, password=credentials.MT5_PASSWORD, server=credentials.MT5_SERVER)
    if not login_status:
        log_message(f"Failed to login to account {credentials.MT5_LOGIN}, error code: {mt5.last_error()}", level=logging.ERROR)
        mt5.shutdown()
        return False

    log_message(f"Logged in to account {credentials.MT5_LOGIN} successfully.")
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
    """Calculate stop loss and take profit levels based on the market structure."""
    try:
        data = load_data(f'../data/{symbol}_H4_data.csv')
        data = preprocess_data(data)  # Ensure data is preprocessed
        support, resistance = calculate_support_resistance(data)

        if support is None or resistance is None:
            log_message(f"Support or resistance levels are None for {symbol}.", level=logging.ERROR)
            return None, None

        if action == 'buy':
            stop_loss = support - 20 * 0.0001
            take_profit = resistance + 500 * 0.0001
        else:
            stop_loss = resistance + 20 * 0.0001
            take_profit = support - 500 * 0.0001

        return stop_loss, take_profit

    except Exception as e:
        log_message(f"Error calculating stop loss and take profit for {symbol}: {str(e)}", level=logging.ERROR)
        return None, None

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

    if not initialize_mt5():
        return

    for symbol in trading_pairs:
        action = 'buy'  # Example action
        stop_loss, take_profit = calculate_stop_loss_and_take_profit(symbol, action)
        if stop_loss and take_profit:
            result = place_order(symbol, action, lot_size, stop_loss, take_profit)
            print(result)

if __name__ == "__main__":
    main()
