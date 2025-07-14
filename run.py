if __name__ == "__main__":
    from core.data_loader import fetch_live_data
    from strategies.alpha_engine import generate_alpha_signals
    from ml.model import predict_trade_signal
    from execution.trade_executor import execute_trade
    from filters.regime import detect_market_regime

    candles = fetch_live_data("XAUUSD", timeframe="15m", lookback=200)

    if len(candles) < 100:
        print("⚠️ Not enough candle data to generate signals.")
    else:
        signals = generate_alpha_signals(candles)
        regime = detect_market_regime(candles)

        features = {
            **signals,
            "regime": regime
        }

        decision = predict_trade_signal(features)
        if decision["trade"]:
            execute_trade(decision)
        else:
            print("[🟡] No Trade Signal at this time.")
