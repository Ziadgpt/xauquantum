import pandas as pd
import numpy as np
from pykalman import KalmanFilter

def kalman_deviation_signal(candles, threshold=2.0):
    close = candles["close"].values

    if len(close) < 50:
        return 0  # Not enough data

    kf = KalmanFilter(initial_state_mean=close[0], n_dim_obs=1)
    state_means, _ = kf.filter(close)

    # Residual = actual - estimated
    residual = close - state_means.flatten()
    zscore = (residual - residual.mean()) / residual.std()
    last_z = zscore[-1]

    if last_z > threshold:
        return -1  # Sell (price way above Kalman)
    elif last_z < -threshold:
        return 1   # Buy (price way below Kalman)
    else:
        return 0
