import MetaTrader5 as mt5
from config.settings import CONFIG
from core.logger import log_trade

def execute_trade(decision):
    symbol = CONFIG["symbol"]
    lot = CONFIG["lot_size"]

    if not mt5.initialize():
        print("❌ Failed to connect to MT5 for execution.")
        return

    # Get latest price data
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ Symbol {symbol} not found.")
        mt5.shutdown()
        return

    if not symbol_info.visible:
        mt5.symbol_select(symbol, True)

    price = mt5.symbol_info_tick(symbol).ask if decision["action"] == "buy" else mt5.symbol_info_tick(symbol).bid

    order_type = mt5.ORDER_TYPE_BUY if decision["action"] == "buy" else mt5.ORDER_TYPE_SELL
    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": deviation,
        "magic": 123456,
        "comment": "XAUQuantum trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Trade failed: {result.retcode}")
    else:
        print("✅ Trade Executed:", result)
        log_trade({
            "symbol": symbol,
            "action": decision["action"],
            "price": price,
            "volume": lot,
            "confidence": decision.get("confidence", 0)
        })
