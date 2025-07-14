import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def fetch_live_data(symbol, timeframe="15m", lookback=200):
    timeframe_map = {
        "15m": mt5.TIMEFRAME_M15,
        "1h": mt5.TIMEFRAME_H1
    }
    tf = timeframe_map.get(timeframe, mt5.TIMEFRAME_M15)

    if not mt5.initialize():
        raise RuntimeError("❌ Could not initialize MT5")

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, lookback)
    mt5.shutdown()

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    return df

def fetch_historical_data(symbol, timeframe="15m", lookback=1500):
    return fetch_live_data(symbol, timeframe, lookback)
