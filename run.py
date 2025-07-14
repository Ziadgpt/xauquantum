if __name__ == "__main__":
    import time
    from core.data_loader import fetch_live_data
    from strategies.alpha_engine import generate_alpha_signals
    from ml.model import predict_trade_signal
    from execution.trade_executor import execute_trade
    from filters.regime import detect_market_regime

    symbol = "XAUUSDc"
    timeframe = "15m"
    lookback = 200

    print(f"[🚀] Starting {symbol} bot...")

    while True:
        candles = fetch_live_data(symbol, timeframe=timeframe, lookback=lookback)

        if candles is None or len(candles) < 100:
            print("⚠️ Not enough candle data to generate signals.")
            time.sleep(60)
            continue

        # === Generate Alpha Signals ===
        signals = generate_alpha_signals(candles)

        # === Market Regime Detection ===
        regime = detect_market_regime(candles)

        # === Combine Features for ML ===
        features = {
            **signals,
            "regime": regime
        }

        # === ML Decision ===
        decision = predict_trade_signal(features)

        if decision["trade"]:
            execute_trade(decision)
        else:
            print("[🟡] No Trade Signal at this time.")

        # === Wait until next 15M candle ===
        time.sleep(900)
