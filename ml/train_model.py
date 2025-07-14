import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Load and prepare data ===
df = pd.read_csv("../labeled_trades.csv")

# Features and label
X = df.drop(columns=["label"])
y = df["label"]

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    stratify=y,
    random_state=42
)

# === Train Model ===
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',  # Handle imbalance
    random_state=42
)
model.fit(X_train, y_train)

# === Save model ===
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/trade_classifier.pkl")

# === Evaluation ===
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, digits=2))

print("\n🧩 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n🔥 ROC AUC Score:", roc_auc_score(y_test, y_proba))

# === Plot ROC Curve ===
fpr, tpr, _ = roc_curve(y_test, y_proba)
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
