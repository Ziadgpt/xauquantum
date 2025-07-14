import pandas as pd

def zscore_reversion_signal(df: pd.DataFrame, window=50, threshold=2.0) -> pd.DataFrame:
    df = df.copy()
    close = df["close"]

    if len(close) < window:
        df["signal_zscore"] = 0
        return df  # Not enough data, no signal

    ma = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    zscore = (close - ma) / std
    last_z = zscore.iloc[-1]

    signal = 0
    if last_z > threshold:
        signal = -1  # Sell signal (price too high)
    elif last_z < -threshold:
        signal = 1   # Buy signal (price too low)

    df["signal_zscore"] = 0
    df.at[df.index[-1], "signal_zscore"] = signal

    return df
