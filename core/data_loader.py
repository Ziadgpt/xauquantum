import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
symbol = "XAUUSDc"
def fetch_live_data(symbol, timeframe="15m", lookback=200):

    tf_map = {
        "1m": mt5.TIMEFRAME_M1,
        "5m": mt5.TIMEFRAME_M5,
        "15m": mt5.TIMEFRAME_M15,
        "1h": mt5.TIMEFRAME_H1,
        "4h": mt5.TIMEFRAME_H4,
        "1d": mt5.TIMEFRAME_D1,
    }

    print(f"[📥] Fetching {lookback} candles for {symbol} ({timeframe})...")

    if not mt5.initialize():
        raise RuntimeError(f"❌ Could not initialize MT5 — {mt5.last_error()}")

    if symbol not in [s.name for s in mt5.symbols_get()]:
        raise ValueError(f"❌ Symbol '{symbol}' not found in MT5 Market Watch")

    bars = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, lookback)

    mt5.shutdown()

    if bars is None or len(bars) == 0:
        raise ValueError("⚠️ No bars returned — check symbol name and chart subscription")

    df = pd.DataFrame(bars)
    if "time" not in df.columns:
        print("❌ 'time' column missing in bars")
        print(df.head())
        raise ValueError("⚠️ Missing 'time' column in DataFrame")

    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df
