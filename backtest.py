import os
import pandas as pd
from strategies.alpha_engine import generate_alpha_signals
from filters.regime import detect_market_regime
from core.data_loader import fetch_live_data

# Ensure output directory exists
os.makedirs("logs", exist_ok=True)

def backtest_and_label(candles, tp_pct=0.002, sl_pct=0.001):
    rows = []

    for i in range(100, len(candles) - 2):  # Skip warmup and out-of-bounds
        window = candles.iloc[:i].copy()
        future = candles.iloc[i + 1:i + 3]  # Lookahead 2 candles

        if len(future) < 2:
            continue

        try:
            signals = generate_alpha_signals(window)
            regime = detect_market_regime(window)
        except Exception as e:
            print(f"⚠️ Error generating features at index {i}: {e}")
            continue

        entry_price = window["close"].iloc[-1]
        high_future = future["high"].max()
        low_future = future["low"].min()

        # Label logic
        if high_future >= entry_price * (1 + tp_pct):
            label = 1
        elif low_future <= entry_price * (1 - sl_pct):
            label = 0
        else:
            label = 0

        row = {
            "rsi_signal": signals.get("rsi_signal", 0),
            "adx_pullback": signals.get("adx_pullback", 0),
            "impulse_signal": signals.get("impulse_signal", 0),
            "zscore_signal": signals.get("zscore_signal", 0),
            "kalman_filter_signal": signals.get("kalman_filter_signal", 0),
            "regime": regime,
            "label": label
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    df.fillna(0, inplace=True)  # Ensure no NaNs
    df.to_csv("logs/labeled_trades.csv", index=False)
    print(f"✅ Backtest complete: {len(df)} samples saved to logs/labeled_trades.csv")

if __name__ == "__main__":
    candles = fetch_live_data("XAUUSDc", timeframe="15m", lookback=2000)
    if candles is not None and len(candles) >= 150:
        backtest_and_label(candles)
    else:
        print("⚠️ Not enough candle data to run backtest.")
