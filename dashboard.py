import streamlit as st
import pandas as pd
import plotly.express as px
import os

def launch_dashboard():
    st.set_page_config(page_title="XAUQuantum Dashboard", layout="wide")
    st.title("📊 XAUQuantum Trading Dashboard")

    LOG_PATH = "logs/trade_log.csv"

    # Handle missing log file
    if not os.path.exists(LOG_PATH):
        st.error("❌ 'logs/trade_log.csv' not found. No trades logged yet.")
        return

    try:
        df = pd.read_csv(LOG_PATH)
    except Exception as e:
        st.error(f"⚠️ Failed to read log file: {e}")
        return

    if df.empty:
        st.warning("⚠️ Trade log is empty.")
        return

    # Process timestamp and equity
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    if "pnl" not in df.columns:
        st.error("❌ Missing 'pnl' column in log file.")
        return

    df["equity"] = df["pnl"].cumsum()

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Equity Curve")
        st.line_chart(df.set_index("timestamp")["equity"])

    with col2:
        st.subheader("🔥 Strategy PnL Breakdown")
        if "strategy" in df.columns:
            strat_pnl = df.groupby("strategy")["pnl"].sum().sort_values()
            st.bar_chart(strat_pnl)
        else:
            st.warning("No 'strategy' column found in log file.")

    st.subheader("📋 Recent Trades")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(10))

    if "confidence" in df.columns and "strategy" in df.columns:
        st.subheader("🎯 Confidence vs. PnL")
        fig = px.scatter(
            df,
            x="confidence",
            y="pnl",
            color="strategy",
            hover_data=["timestamp"],
            title="Model Confidence vs. Trade Outcome",
        )
        st.plotly_chart(fig)
    else:
        st.info("Add 'confidence' and 'strategy' to log for scatter chart.")

