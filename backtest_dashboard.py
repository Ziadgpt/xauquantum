import pandas as pd
import streamlit as st
import plotly.express as px

# Load backtest results
df = pd.read_csv("logs/labeled_trades.csv")

st.set_page_config(layout="wide")
st.title("📊 XAUQuantum Backtest Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏁 Trade Label Distribution")
    st.plotly_chart(px.histogram(df, x="label", color="label", nbins=3))

with col2:
    st.subheader("📉 Regime Distribution")
    st.plotly_chart(px.histogram(df, x="regime", color="regime"))

# Feature inspection
st.subheader("📌 Signal Breakdown")

for col in ["rsi_signal", "adx_pullback", "impulse_signal"]:
    fig = px.histogram(df, x=col, color=df["label"].astype(str), barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Heatmap
st.subheader("🧠 Feature vs Label Correlation")

numeric_cols = ["rsi_signal", "adx_pullback", "impulse_signal", "regime"]
cor = df[numeric_cols + ["label"]].corr()

fig = px.imshow(cor, text_auto=True, aspect="auto", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

st.caption("Made with ❤️ by XAUQuantum")
