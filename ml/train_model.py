import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv("logs/labeled_trades.csv")

if len(df) < 10:
    raise ValueError("Not enough data to train model.")

features = [
    "rsi_signal",
    "macd_bb_signal",
    "structure_signal",
    "zscore_signal",
    "kalman_filter_signal",
    "regime"
]

for f in features:
    if f not in df.columns:
        raise ValueError(f"Missing feature column: {f}")

X = df[features]
y = df["label"]

print("Label distribution:\n", y.value_counts())

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
except ValueError:
    print("⚠️ Stratified split failed. Using simple split.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

model = xgb.XGBClassifier(
    n_estimators=150,
    max_depth=6,
    scale_pos_weight=y.value_counts()[0] / y.value_counts()[1],
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)

model.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/xauquantum_model.pkl")

y_pred = model.predict(X_test)

if len(set(y_test)) == 2:
    y_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    fpr, tpr, _ = roc_curve(y_test, y_proba)

    print("\n🔥 ROC AUC Score:", round(auc, 3))

    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, label="ROC Curve", color="green")
    plt.plot([0, 1], [0, 1], "--", color="gray")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig("models/roc_curve.png")
    plt.close()
else:
    print("⚠️ ROC AUC skipped: only one class in test data.")

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, digits=2))

print("\n🧩 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
