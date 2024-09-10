# app.py (Flask setup for front-end)
from flask import Flask, render_template, jsonify
import trade_executor  # Assuming you import your backend logic here
import subprocess

app = Flask(__name__)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for triggering a trade (backend functionality)
@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    # Call your backend function to execute a trade
    result = trade_executor.execute_trade()
    return jsonify({'status': 'Trade Executed', 'result': result})

# Route for getting trade status
@app.route('/trade_status', methods=['GET'])
def trade_status():
    status = trade_executor.get_trade_status()  # Assume this function returns current status
    return jsonify({'status': status})

if __name__ == '__main__':
    # Run your backend trading logic in parallel with Flask
    subprocess.Popen(["python", "main.py"])
    app.run(debug=True)
