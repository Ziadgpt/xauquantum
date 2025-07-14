import pandas as pd

def impulse_detector_signal(candles, atr_period=14, impulse_multiplier=1.5):
    high = candles["high"]
    low = candles["low"]
    close = candles["close"]

    # True Range & ATR
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window=atr_period).mean()
    last_atr = atr.iloc[-1]
    last_range = high.iloc[-1] - low.iloc[-1]

    # Range explosion
    impulse_candle = last_range > impulse_multiplier * last_atr

    # Directional conviction
    close_pos = (close.iloc[-1] - low.iloc[-1]) / (high.iloc[-1] - low.iloc[-1] + 1e-9)

    if impulse_candle and close_pos > 0.8:
        return 1  # Long impulse
    elif impulse_candle and close_pos < 0.2:
        return -1  # Short impulse
    else:
        return 0
