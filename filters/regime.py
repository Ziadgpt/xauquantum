import pandas as pd
from hmmlearn.hmm import GaussianHMM
import numpy as np
def detect_market_regime(df, window=100):
    returns = df["close"].pct_change().dropna()[-window:]
    returns = returns.replace([np.inf, -np.inf], np.nan).dropna()

    if len(returns) < window:
        return -1  # Fallback if not enough clean data

    model = GaussianHMM(n_components=2, covariance_type="full", n_iter=100)
    try:
        model.fit(returns.values.reshape(-1, 1))
        hidden_states = model.predict(returns.values.reshape(-1, 1))
        return hidden_states[-1]  # return most recent state
    except Exception as e:
        print(f"⚠️ Regime detection failed: {e}")
        return -1