from flask import Flask, request, send_from_directory, jsonify
import os
import json
import logging
import sys
import MetaTrader5 as mt5

# Add the trade_manager directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'trade_manager')))

# Import necessary functions from trade_executor
from trade_executor import load_config, initialize_mt5, place_order, calculate_stop_loss_and_take_profit

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'frontend'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/data')
def get_data():
    # Example logic to fetch data
    config = load_config('config/config.json')
    if not config:
        return jsonify({'error': 'Configuration error'}), 500

    # Example: Return some dummy data
    return jsonify({'data': 'sample data from trading bot'})

@app.route('/market_data/EURUSD')
def market_data_eurusd():
    # Initialize MetaTrader 5
    if not mt5.initialize():
        return jsonify({'error': 'Failed to initialize MT5'}), 500

    # Get EURUSD tick data
    symbol_info = mt5.symbol_info_tick("EURUSD")
    if symbol_info is None:
        return jsonify({'error': 'Failed to get symbol info'}), 500

    data = {
        "symbol": "EURUSD",
        "bid": symbol_info.bid,
        "ask": symbol_info.ask,
        "volume": symbol_info.volume
    }
    return jsonify(data)

@app.route('/api/place_order', methods=['POST'])
def place_order_api():
    data = json.loads(request.data)
    symbol = data.get('symbol')
    action = data.get('action')
    lot_size = data.get('lot_size')
    stop_loss = data.get('stop_loss')
    take_profit = data.get('take_profit')

    if not symbol or not action or not lot_size or stop_loss is None or take_profit is None:
        return jsonify({'error': 'Invalid input'}), 400

    logging.info(f"Placing order: symbol={symbol}, action={action}, lot_size={lot_size}, stop_loss={stop_loss}, take_profit={take_profit}")

    result = place_order(symbol, action, lot_size, stop_loss, take_profit)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        return jsonify({'status': 'success', 'message': 'Order placed successfully', 'result': str(result)})
    else:
        logging.error(f"Order placement failed: {result}")
        return jsonify({'error': 'Order placement failed', 'details': str(result)}), 500

if __name__ == '__main__':
    app.run(debug=True)
