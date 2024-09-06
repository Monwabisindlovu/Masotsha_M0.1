from sklearn.linear_model import LinearRegression
import numpy as np
from data.historical_data import load_data, preprocess_data
from utils.logger import log_message

def learn_market_movement(data):
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

def check_entry_conditions(symbol, timeframe):
    try:
        data = load_data(f'data/{timeframe}_data.csv')
        data = preprocess_data(data)
        data = learn_market_movement(data)
        
        latest_price = data['close'].iloc[-1]
        predicted_direction = data['predicted_direction'].iloc[-1]
        
        if predicted_direction > 0.5:
            return 'buy'
        else:
            return 'sell'
    except Exception as e:
        log_message(f"Error checking entry conditions for {symbol}: {str(e)}")
    return None
