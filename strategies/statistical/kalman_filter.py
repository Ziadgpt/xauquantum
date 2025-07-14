import pandas as pd
import numpy as np
from pykalman import KalmanFilter

def kalman_deviation_signal(df: pd.DataFrame, threshold=2.0) -> pd.DataFrame:
    df = df.copy()

    close = df["close"].values

    if len(close) < 50:
        df["kalman_deviation_signal"] = 0
        return df

    kf = KalmanFilter(initial_state_mean=close[0], n_dim_obs=1)
    state_means, _ = kf.filter(close)

    residual = close - state_means.flatten()
    zscore = (residual - residual.mean()) / residual.std()
    last_z = zscore[-1]

    if last_z > threshold:
        signal = -1
    elif last_z < -threshold:
        signal = 1
    else:
        signal = 0

    # Add the signal as a new column for all rows, but typically signal applies to last row only
    # You can fill all rows with 0 except last, or just set last row signal and fill rest 0
    df["kalman_deviation_signal"] = 0
    df.at[df.index[-1], "kalman_deviation_signal"] = signal

    return df
