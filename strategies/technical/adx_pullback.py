import pandas as pd
import numpy as np

def adx_pullback_signal(candles, adx_period=14, pullback_ema=20, adx_threshold=20):
    """
    Returns:
        1 → Long (pullback in uptrend)
       -1 → Short (pullback in downtrend)
        0 → No trade
    """
    high = candles["high"]
    low = candles["low"]
    close = candles["close"]

    # Calculate EMA for pullback zone
    ema = close.ewm(span=pullback_ema, adjust=False).mean()

    # +DM, -DM
    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    # True Range
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(adx_period).mean()
    plus_di = 100 * (plus_dm.rolling(adx_period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(adx_period).mean() / atr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(adx_period).mean()

    # Check trend + pullback
    last_adx = adx.iloc[-1]
    last_price = close.iloc[-1]
    last_ema = ema.iloc[-1]

    # Uptrend pullback
    if last_adx > adx_threshold and close.iloc[-1] > ema.iloc[-1] and close.iloc[-2] < ema.iloc[-2]:
        return 1
    # Downtrend pullback
    elif last_adx > adx_threshold and close.iloc[-1] < ema.iloc[-1] and close.iloc[-2] > ema.iloc[-2]:
        return -1
    else:
        return 0
