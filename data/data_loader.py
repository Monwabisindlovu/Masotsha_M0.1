import pandas as pd

def load_data(filename):
    try:
        return pd.read_csv(filename)
    except Exception as e:
        log_message(f"Error loading data from {filename}: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def preprocess_data(df):
    try:
        # Add any preprocessing steps here if needed
        return df
    except Exception as e:
        log_message(f"Error preprocessing data: {str(e)}")
        return df
