import pandas as pd
from hmmlearn.hmm import GaussianHMM
import numpy as np

def detect_market_regime(candles, n_states=3, window=100):
    close = candles["close"].copy()
    returns = close.pct_change().dropna().values.reshape(-1, 1)

    if len(returns) < window:
        return 1  # Default neutral regime

    model = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000)
    model.fit(returns[-window:])
    hidden_states = model.predict(returns[-window:])

    # Use the most recent hidden state as current regime
    current_regime = hidden_states[-1]
    return current_regime
