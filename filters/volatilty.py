import pandas as pd
import numpy as np

try:
    from arch import arch_model
    GARCH_AVAILABLE = True
except ImportError:
    print("⚠️ GARCH model (arch) not available, falling back to rolling volatility.")
    GARCH_AVAILABLE = False

def forecast_volatility(df, price_col="close", horizon=1, fallback=True):
    try:
        # Step 1: Preprocess price series
        series = df[price_col].astype(float).pct_change().dropna() * 100

        # Step 2: Not enough data
        if len(series) < 30:
            raise ValueError("Not enough data for GARCH.")

        # Step 3: Run GARCH if available
        if GARCH_AVAILABLE:
            model = arch_model(series, vol='Garch', p=1, q=1, rescale=True)
            res = model.fit(disp="off")
            forecast = res.forecast(horizon=horizon)
            vol_forecast = forecast.variance.values[-1][0] ** 0.5
            return vol_forecast / 100  # return as decimal, e.g. 0.015
        else:
            raise ImportError("arch module not available.")

    except Exception as e:
        print(f"⚠️ GARCH failed: {e}")

        if fallback:
            # Optional: Use rolling std deviation as a fallback
            fallback_vol = series.rolling(14).std().iloc[-1]
            print(f"🔁 Using fallback rolling volatility: {fallback_vol / 100:.4f}")
            return fallback_vol / 100
        else:
            return np.nan
