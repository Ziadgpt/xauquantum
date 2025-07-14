import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def fetch_live_data(symbol, timeframe="15m", lookback=200):
    if not mt5.initialize():
        raise Exception("❌ MT5 initialization failed.")

    tf_map = {
        "1m": mt5.TIMEFRAME_M1,
        "5m": mt5.TIMEFRAME_M5,
        "15m": mt5.TIMEFRAME_M15,
        "1h": mt5.TIMEFRAME_H1,
        "4h": mt5.TIMEFRAME_H4,
        "1d": mt5.TIMEFRAME_D1,
    }

    bars = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, lookback)
    mt5.shutdown()

    df = pd.DataFrame(bars)
    if df.empty or "time" not in df.columns:
        raise ValueError("⚠️ Failed to load live data.")

    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df
