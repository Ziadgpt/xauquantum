import pandas as pd

def rsi2_signal(candles, rsi_period=2, oversold=10, overbought=90):
    close = candles["close"]
    delta = close.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    last_rsi = rsi.iloc[-1]

    if last_rsi < oversold:
        return 1  # Long signal
    elif last_rsi > overbought:
        return -1  # Short signal
    else:
        return 0  # No trade
