import joblib
import numpy as np

MODEL_PATH = "models/xauquantum_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def predict_trade_signal(signals, regime=None, volatility=None):
    model = load_model()

    features = np.array([[
        signals.get("rsi_signal", 0),
        signals.get("macd_bb_signal", 0),
        signals.get("structure_signal", 0),
        signals.get("zscore_signal", 0),
        signals.get("kalman_filter_signal", 0),
        regime if regime is not None else 1,
        volatility if volatility is not None else 0.01
    ]])

    proba = model.predict_proba(features)[0][1]

    return {
        "trade": proba > 0.6,
        "confidence": round(proba, 4)
    }
