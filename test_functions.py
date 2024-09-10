import sys
import os
import logging

# Set the project root directory explicitly
project_root = r'C:\Users\monwa\Masotsha_M0.1'
sys.path.append(project_root)

from strategy.market_structure import load_data
from trade_manager.risk_management import calculate_take_profit, calculate_stop_loss, calculate_support_resistance
from trade_manager.logger import log_message, setup_logger

def test_functions():
    setup_logger()  # Initialize logging

    symbol = 'AAPL'
    entry_price = 150.00  # Example entry price
    direction = 'buy'
    pips = 500

    print("Testing calculate_take_profit:")
    take_profit = calculate_take_profit(entry_price, direction, pips)
    print(f"Take Profit: {take_profit}")

    print("Testing calculate_stop_loss:")
    support_resistance = 148.00  # Example support/resistance level
    stop_loss = calculate_stop_loss(entry_price, direction, support_resistance, pips=20)
    print(f"Stop Loss: {stop_loss}")

    print("Testing calculate_support_resistance:")
    data = load_data(f'{project_root}/data/AAPL_H4_data.csv')  # Example data file path
    support, resistance = calculate_support_resistance(data)
    print(f"Support: {support}, Resistance: {resistance}")

if __name__ == "__main__":
    test_functions()
