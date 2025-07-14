import streamlit as st
import pandas as pd
import plotly.express as px

def launch_dashboard():
    st.set_page_config(page_title="XAUQuantum Dashboard", layout="wide")
    st.title("📊 XAUQuantum Trading Dashboard")

    df = pd.read_csv("logs/trade_log.csv")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Equity Curve")
        df["equity"] = df["pnl"].cumsum()
        st.line_chart(df.set_index("timestamp")["equity"])

    with col2:
        st.subheader("Strategy Heatmap")
        heatmap = df.groupby("strategy")["pnl"].sum()
        st.bar_chart(heatmap)

    st.subheader("Recent Trades")
    st.dataframe(df.tail(10))

    st.subheader("Confidence vs. PnL")
    fig = px.scatter(df, x="confidence", y="pnl", color="strategy")
    st.plotly_chart(fig)
