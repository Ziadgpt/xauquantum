# 🧠 XAUQuantum — Institutional-Grade XAUUSD Trading Bot

**XAUQuantum** is a modular, alpha-expanding trading system for XAUUSD, combining:

- 📉 Technical + Statistical Alphas
- 🔍 Regime Detection (HMM)
- ⚡ GARCH Volatility Filtering
- 🤖 ML Signal Decision (XGBoost)
- 💻 Real-time Dashboard (Streamlit)
- 💹 Executable via MetaTrader 5 API

---

## 🚀 Components

| Module       | Purpose                           |
|--------------|------------------------------------|
| `strategies/` | RSI2, ADX Pullback, Z-score, Kalman |
| `ml/`         | Train & Predict ML signals         |
| `filters/`    | Volatility + Regime detection      |
| `execution/`  | Broker-side execution (via MT5)    |
| `dashboard/`  | Real-time monitoring interface      |
| `backtest/`   | Offline backtesting + labeling      |

---

## 📦 Setup

```bash
git clone https://github.com/yourusername/xauquantum.git
cd xauquantum
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
