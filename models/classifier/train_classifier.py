from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "isolation_results.csv"

MODEL_DIR = BASE_DIR / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "attack_classifier.pkl"
DASHBOARD_DATA_DIR = BASE_DIR / "dashboard" / "data"
PREDICTIONS_PATH = DASHBOARD_DATA_DIR / "predictions.csv"

# ----------------------------
# Load Data
# ----------------------------

df = pd.read_csv(INPUT_FILE)

features = [
    "session_duration",
    "failed_attempts",
    "login_hour",
    "day_of_week",
    "resource_sensitivity",
    "device_trust_score",
    "login_frequency",
    "behavior_score",
    "risk_score",
    "high_failed_login",
    "long_session"
]

X = df[features]

y = df["label"]

# ----------------------------
# Train/Test Split
# ----------------------------

train_idx, test_idx = train_test_split(
    df.index,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train = X.loc[train_idx]
X_test = X.loc[test_idx]
y_train = y.loc[train_idx]
y_test = y.loc[test_idx]
df_test = df.loc[test_idx].copy()

# ----------------------------
# Model
# ----------------------------

clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

clf.fit(X_train, y_train)

# ----------------------------
# Evaluation
# ----------------------------

pred = clf.predict(X_test)

print("="*60)
print("Classification Accuracy")
print("="*60)

print(accuracy_score(y_test, pred))

print()

print(classification_report(y_test, pred, zero_division=0))

output = df_test.copy()

output["Actual"] = y_test.values
output["Predicted"] = pred

if hasattr(clf, "predict_proba"):
    output["Confidence"] = clf.predict_proba(X_test).max(axis=1)
else:
    output["Confidence"] = 1.0

DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

output.to_csv(PREDICTIONS_PATH, index=False)

print("\nPredictions exported successfully.")

joblib.dump(clf, MODEL_PATH)

print("\nModel Saved:", MODEL_PATH)
