import MetaTrader5 as mt5
from config.settings import CONFIG
from core.logger import log_trade

def execute_trade(decision):
    symbol = CONFIG["symbol"]
    lot = CONFIG["lot_size"]

    if not mt5.initialize():
        print("❌ Failed to connect to MT5 for execution.")
        return

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ Symbol {symbol} not found.")
        mt5.shutdown()
        return

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"❌ Failed to select symbol {symbol}.")
            mt5.shutdown()
            return

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Failed to get tick for {symbol}.")
        mt5.shutdown()
        return

    price = tick.ask if decision["action"].lower() == "buy" else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if decision["action"].lower() == "buy" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": 123456,
        "comment": "XAUQuantum trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Trade failed with retcode={result.retcode}")
        # Optionally add detailed error explanation here
    else:
        print(f"✅ Trade executed successfully: {result}")
        log_trade({
            "symbol": symbol,
            "action": decision["action"],
            "price": price,
            "volume": lot,
            "confidence": decision.get("confidence", 0),
            "order_id": result.order
        })
