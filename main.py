from flask import Flask, request, send_from_directory, jsonify
import os
import json
import logging
import MetaTrader5 as mt5
from trade_manager.trade_executor import load_config, initialize_mt5, place_order, calculate_stop_loss_and_take_profit

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
    # This should be replaced with actual data fetching logic
    config = load_config('config/config.json')
    if not config:
        return jsonify({'error': 'Configuration error'}), 500

    # Example: Return some dummy data
    return jsonify({'data': 'sample data from trading bot'})

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

    result = place_order(symbol, action, lot_size, stop_loss, take_profit)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        return jsonify({'status': 'success', 'result': str(result)})
    else:
        return jsonify({'error': 'Order placement failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)