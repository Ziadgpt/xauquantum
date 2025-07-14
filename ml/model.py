import joblib
import numpy as np

MODEL_PATH = "models/xauquantum_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def predict_trade_signal(signals, regime=None, volatility=None):
    model = load_model()

    features = np.array([[
        signals["rsi_signal"],
        signals["adx_pullback"],
        signals["impulse_signal"],
        regime if regime is not None else 1,
        volatility if volatility is not None else 0.01
    ]])

    proba = model.predict_proba(features)[0][1]  # Probability of class 1 = trade

    return {
        "trade": proba > 0.6,
        "confidence": round(proba, 4)
    }
