import csv
import os
from datetime import datetime

def log_trade(trade_info, log_path="logs/trade_log.csv"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    trade_info["timestamp"] = datetime.utcnow().isoformat()
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trade_info.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(trade_info)
    print("📝 Trade logged:", trade_info)
