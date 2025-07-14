from strategies.technical.momentum import apply_rsi2
from strategies.technical.macd_bollinger import apply_macd_bollinger
from strategies.technical.structure_breakout import detect_hh_ll_breakout
from strategies.statistical.zscore import zscore_reversion_signal
from strategies.statistical.kalman_filter import kalman_deviation_signal


def generate_alpha_signals(df):
    df = apply_rsi2(df)
    print(type(df))  # should be pd.DataFrame
    df = apply_macd_bollinger(df)
    print(type(df))
    df = detect_hh_ll_breakout(df)
    print(type(df))
    df = zscore_reversion_signal(df)
    print(type(df))
    df = kalman_deviation_signal(df)
    print(type(df))  # If this is int, problem!

    return {
        "rsi_signal": df.iloc[-1].get("signal", 0),
        "macd_bb_signal": df.iloc[-1].get("signal_macd_bb", 0),
        "structure_signal": df.iloc[-1].get("signal_structure", 0),
        "zscore_signal": df.iloc[-1].get("signal_zscore", 0),
        "kalman_filter_signal": df.iloc[-1].get("kalman_deviation_signal", 0),
    }
