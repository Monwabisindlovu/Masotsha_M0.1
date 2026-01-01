import json
import logging
import time
import MetaTrader5 as mt5

from trade_manager.trade_executor import (
    load_config,
    initialize_mt5,
    place_order,
    calculate_stop_loss_and_take_profit
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run_bot():
    logging.info("Starting Masotsha_M0.1 Trading Bot")

    # Load config
    config = load_config('config/config.json')
    if not config:
        logging.error("Failed to load config.json")
        return

    lot_size = config.get("LOT_SIZE", 0.01)
    trading_pairs = config.get("TRADING_PAIRS", ["EURUSD"])
    max_trades_per_day = config.get("MAX_TRADES_PER_DAY", 1)
    max_positions_per_trade = config.get("MAX_POSITIONS_PER_TRADE", 1)

    # Initialize MT5
    if not initialize_mt5():
        logging.error("MT5 initialization failed")
        return

    trades_taken = 0

    for symbol in trading_pairs:
        if trades_taken >= max_trades_per_day:
            break

        action = "buy"  # replace later with strategy logic

        stop_loss, take_profit = calculate_stop_loss_and_take_profit(
            symbol, action
        )

        if stop_loss is None or take_profit is None:
            logging.warning(f"Skipping {symbol}: SL/TP calculation failed")
            continue

        for _ in range(max_positions_per_trade):
            result = place_order(
                symbol=symbol,
                action=action,
                lot_size=lot_size,
                stop_loss=stop_loss,
                take_profit=take_profit
            )

            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                trades_taken += 1
                logging.info(f"Trade placed successfully on {symbol}")
            else:
                logging.error(f"Failed to place trade on {symbol}")

            if trades_taken >= max_trades_per_day:
                break

            time.sleep(2)

    mt5.shutdown()
    logging.info("Masotsha_M0.1 Bot execution finished")


if __name__ == "__main__":
    run_bot()
