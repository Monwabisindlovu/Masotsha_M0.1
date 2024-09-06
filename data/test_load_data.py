# File: data/test_load_data.py

import pandas as pd

def test_load():
    try:
        # Attempt to read the CSV file
        data = pd.read_csv('data/EURUSD_H4_data.csv')
        print(data)
    except Exception as e:
        # Print any errors that occur
        print(f"Error reading file: {str(e)}")

# Run the test
test_load()
