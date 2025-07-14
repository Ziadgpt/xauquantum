import streamlit as st
import pandas as pd
import plotly.graph_objs as go

from core.data_loader import fetch_live_data
from strategies.alpha_engine import generate_alpha_signals
from ml.model import predict_trade_signal
from filters.regime import detect_market_regime
from config.settings import CONFIG

st.set_page_config(page_title="XAUQuantum Dashboard", layout="wide")

st.title("💎 XAUQuantum Dashboard")

# Load live data
candles = fetch_live_data(CONFIG["symbol"], timeframe="15m", lookback=150)
signals = generate_alpha_signals(candles)
regime = detect_market_regime(candles)
decision = predict_trade_signal(signals, regime)

# === Chart ===
st.subheader("📈 XAUUSD Price (15m)")
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=candles.index,
    open=candles["open"],
    high=candles["high"],
    low=candles["low"],
    close=candles["close"],
    name="Candles"
))
fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

# === Signal Table ===
st.subheader("📊 Alpha Signals")
st.write(pd.DataFrame([signals]))

# === Regime + Volatility ===
st.subheader("📉 Market Conditions")
st.metric("Market Regime", str(regime))

# === ML Decision ===
st.subheader("🤖 ML Trade Decision")
st.write({
    "Should Trade?": "✅ YES" if decision["trade"] else "❌ NO",
    "Confidence": decision["confidence"]
})

st.markdown("---")
st.caption("Powered by MetaTrader5, XGBoost, and Streamlit.")
