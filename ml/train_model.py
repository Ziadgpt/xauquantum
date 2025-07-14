import pandas as pd
import xgboost as xgb
import joblib
import os

def train_model(data_path="logs/labeled_trades.csv", model_path="models/xauquantum_model.pkl"):
    df = pd.read_csv(data_path)

    required_cols = ["rsi_signal", "adx_pullback", "impulse_signal", "volatility", "regime", "label"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Missing required columns in training data.")

    X = df[["rsi_signal", "adx_pullback", "impulse_signal", "volatility", "regime"]]
    y = df["label"]

    model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
    model.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"✅ Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
