import MetaTrader5 as mt5
import logging

# MetaTrader 5 credentials
MT5_LOGIN = 5029867624
MT5_PASSWORD = '@dX1BtDz'
MT5_SERVER = 'MetaQuotes-Demo'

# Path to MetaTrader 5 executable
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_mt5():
    """Initialize the MetaTrader 5 connection."""
    logger.info(f"Initializing MetaTrader 5 from path: {MT5_PATH}")

    # Attempt to initialize MetaTrader 5 with specified path
    if not mt5.initialize(path=MT5_PATH):
        logger.error(f"Failed to initialize MetaTrader 5, error code: {mt5.last_error()}")
        return False

    # Log in to the account
    login_status = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    if not login_status:
        logger.error(f"Failed to login to account {MT5_LOGIN}, error code: {mt5.last_error()}")
        mt5.shutdown()
        return False

    logger.info(f"Logged in to account {MT5_LOGIN} successfully.")
    return True

def main():
    """Main execution function."""
    if initialize_mt5():
        logger.info("MT5 connection and login test successful.")
        mt5.shutdown()
    else:
        logger.error("MT5 connection or login test failed.")

if __name__ == "__main__":
    main()
