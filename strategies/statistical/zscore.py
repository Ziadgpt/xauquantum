import pandas as pd

def zscore_reversion_signal(candles, window=50, threshold=2.0):
    close = candles["close"]

    if len(close) < window:
        return 0  # Not enough data

    ma = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    zscore = (close - ma) / std
    last_z = zscore.iloc[-1]

    if last_z > threshold:
        return -1  # Sell signal (price too high)
    elif last_z < -threshold:
        return 1   # Buy signal (price too low)
    else:
        return 0  # No signal
