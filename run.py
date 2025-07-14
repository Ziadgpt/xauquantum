if __name__ == "__main__":
    from core.data_loader import fetch_live_data
    from strategies.alpha_engine import generate_alpha_signals
    from ml.model import predict_trade_signal
    from execution.trade_executor import execute_trade
    from filters.volatility import forecast_volatility
    from filters.regime import detect_market_regime
    from config.settings import CONFIG

    print("[🚀] Starting XAUQuantum bot...")

    # 1. Fetch candles
    candles = fetch_live_data(CONFIG["symbol"], timeframe="15m", lookback=200)
    print(f"[✅] Loaded {len(candles)} candles for {CONFIG['symbol']}")

    # 2. Forecast volatility
    forecasted_vol = forecast_volatility(candles)
    print(f"[📉] Forecasted Volatility: {forecasted_vol:.2%}")

    if forecasted_vol > CONFIG["volatility_threshold"]:
        print("[🟥] Volatility too high, skipping trade.")
    else:
        # 3. Detect market regime
        regime = detect_market_regime(candles)
        print(f"[🧭] Market Regime: {regime}")

        # 4. Generate alpha signals
        signals = generate_alpha_signals(candles)
        print("[📊] Signals:", signals)

        # 5. ML model decision
        decision = predict_trade_signal(signals, regime, forecasted_vol)
        print(f"[🤖] ML Decision: {decision}")

        # 6. Execute trade
        if decision["trade"]:
            execute_trade(decision)
        else:
            print("[🟡] No Trade Signal at this time.")

    print("[✅] Session Ended")
