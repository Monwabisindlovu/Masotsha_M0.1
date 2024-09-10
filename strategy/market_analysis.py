from turtle import pd
from sklearn.linear_model import LinearRegression
import numpy as np
from data.historical_data import load_data, preprocess_data
from trade_manager.logger import log_message
import logging

def learn_market_movement(data):
    """Learn market movement using historical data."""
    try:
        data['returns'] = data['close'].pct_change()
        data['direction'] = np.where(data['returns'] > 0, 1, 0)
        data['sma'] = data['close'].rolling(window=50).mean()
        data['signal'] = np.where(data['close'] > data['sma'], 1, 0)
        
        X = data[['sma', 'signal']].shift().dropna()
        y = data['direction'].shift(-1).dropna()
        
        model = LinearRegression()
        model.fit(X, y)
        
        data['predicted_direction'] = model.predict(data[['sma', 'signal']])
        return data
    except Exception as e:
        log_message(f"Error learning market movement: {str(e)}", level=logging.ERROR)
        return pd.DataFrame()

def check_entry_conditions(symbol, timeframe):
    """Check entry conditions based on learned market movement."""
    try:
        # Load and preprocess data
        data = load_data(f'data/{symbol}_{timeframe}_data.csv')
        data = preprocess_data(data)
        
        # Learn market movement
        data = learn_market_movement(data)
        
        # Determine entry conditions
        latest_price = data['close'].iloc[-1]
        predicted_direction = data['predicted_direction'].iloc[-1]
        
        if predicted_direction > 0.5:
            return 'buy'
        else:
            return 'sell'
    except Exception as e:
        log_message(f"Error checking entry conditions for {symbol}: {str(e)}", level=logging.ERROR)
    return None
