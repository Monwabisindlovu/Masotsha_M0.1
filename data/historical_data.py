import pandas as pd
import logging
from trade_manager.logger import log_message

def load_data(filename):
    """Load data from a CSV file."""
    try:
        # Read CSV file into DataFrame
        data = pd.read_csv(filename)

        # Check if the DataFrame is empty and log a warning
        if data.empty:
            log_message(f"Loaded data from {filename} is empty.", level=logging.WARNING)
        else:
            log_message(f"Data loaded successfully from {filename}")
        return data

    except FileNotFoundError:
        # Log if file is not found
        log_message(f"File not found: {filename}", level=logging.ERROR)
        return pd.DataFrame()  # Return an empty DataFrame on error

    except pd.errors.EmptyDataError:
        # Log if file is empty or corrupted
        log_message(f"Empty data file: {filename}", level=logging.ERROR)
        return pd.DataFrame()

    except Exception as e:
        # Log any other exceptions that occur
        log_message(f"Error loading data from {filename}: {str(e)}", level=logging.ERROR)
        return pd.DataFrame()

def preprocess_data(data):
    """Preprocess the historical data."""
    # Debugging: Print the column names to ensure 'time' column exists
    print("Columns in the data:", data.columns)  

    # Ensure 'time' column is in datetime format
    if 'time' in data.columns:
        data['time'] = pd.to_datetime(data['time'])
    else:
        log_message(f"'time' column not found in data.", level=logging.ERROR)
        return pd.DataFrame()  # Return an empty DataFrame if 'time' column is missing

    # Drop rows with NaN values
    data = data.dropna()

    return data
