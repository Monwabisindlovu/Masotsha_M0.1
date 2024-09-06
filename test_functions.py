import sys
import os

# Set the project root directory explicitly
project_root = r'C:\Users\monwa\Masotsha_M0.1'
sys.path.append(project_root)

from trade_manager.risk_management import calculate_take_profit, calculate_stop_loss_resistance, calculate_support_resistance

def test_functions():
    symbol = 'AAPL'
    direction = 'buy'
    pips = 500

    print("Testing calculate_take_profit:")
    take_profit = calculate_take_profit(symbol, direction, pips)
    print(f"Take Profit: {take_profit}")

    print("Testing calculate_stop_loss_resistance:")
    stop_loss = calculate_stop_loss_resistance()
    print(f"Stop Loss: {stop_loss}")

    print("Testing calculate_support_resistance:")
    support_resistance = calculate_support_resistance()
    print(f"Support/Resistance: {support_resistance}")

if __name__ == "__main__":
    test_functions()
