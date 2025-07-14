import os
import pandas as pd
from strategies.alpha_engine import generate_alpha_signals
from filters.regime import detect_market_regime
from core.data_loader import fetch_live_data

os.makedirs("logs", exist_ok=True)  # ✅ Ensure 'logs/' folder exists

def backtest_and_label(candles, tp_pct=0.002, sl_pct=0.001):
    rows = []

    for i in range(100, len(candles) - 2):  # Skip warmup and out-of-bounds
        window = candles.iloc[:i].copy()
        future = candles.iloc[i + 1:i + 3]  # Lookahead 2 candles

        if len(future) < 2:
            continue

        signals = generate_alpha_signals(window)
        regime = detect_market_regime(window)
        entry_price = window["close"].iloc[-1]
        high_future = future["high"].max()
        low_future = future["low"].min()

        label = 0
        if high_future >= entry_price * (1 + tp_pct):
            label = 1
        elif low_future <= entry_price * (1 - sl_pct):
            label = 0

        rows.append({
            "rsi_signal": signals["rsi_signal"],
            "adx_pullback": signals["adx_pullback"],
            "impulse_signal": signals["impulse_signal"],
            "regime": regime,
            "label": label
        })

    df = pd.DataFrame(rows)
    df.to_csv("logs/labeled_trades.csv", index=False)
    print(f"✅ Backtest complete: {len(df)} samples saved to logs/labeled_trades.csv")

if __name__ == "__main__":
    from core.data_loader import fetch_live_data

    candles = fetch_live_data("XAUUSDc", timeframe="15m", lookback=2000)
    backtest_and_label(candles)
