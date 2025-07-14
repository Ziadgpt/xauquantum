from strategies.statistical.kalman_filter import kalman_deviation_signal
from strategies.technical.rsi2 import rsi2_signal
from strategies.technical.impulse_detector import impulse_detector_signal
from strategies.technical.adx_pullback import adx_pullback_signal
from strategies.statistical.zscore_reversion import zscore_reversion_signal

def generate_alpha_signals(candles):
    return {
        "rsi_signal": rsi2_signal(candles),
        "adx_pullback": adx_pullback_signal(candles),
        "impulse_signal": impulse_detector_signal(candles),
        "zscore_signal": zscore_reversion_signal(candles),
        "kalman_dev": kalman_deviation_signal(candles),

    }
