import os

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if os.path.isfile(MT5_PATH):
    print(f"Path is correct and accessible: {MT5_PATH}")
else:
    print(f"Path is incorrect or file is not accessible: {MT5_PATH}")
