import pandas as pd
from arch import arch_model

def forecast_volatility(candles, vol_window=50):
    """
    Fits a GARCH(1,1) model to recent returns and forecasts the next period's volatility.
    Returns the annualized forecasted volatility.
    """
    close = candles["close"]
    returns = 100 * close.pct_change().dropna()  # percentage returns

    if len(returns) < vol_window:
        return 0.0  # Not enough data

    model = arch_model(returns[-vol_window:], vol='Garch', p=1, q=1)
    fitted_model = model.fit(disp='off')
    forecast = fitted_model.forecast(horizon=1)
    forecasted_var = forecast.variance.values[-1, 0]
    forecasted_vol = (forecasted_var ** 0.5) / 100  # convert back to decimal

    return forecasted_vol
