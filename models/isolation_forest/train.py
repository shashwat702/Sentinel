import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "baseline_logs.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "isolation_results.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv(INPUT_FILE)

# -----------------------------
# Features used for anomaly detection
# -----------------------------

feature_columns = [
    "session_duration",
    "failed_attempts",
    "login_hour",
    "day_of_week",
    "resource_sensitivity",
    "device_trust_score",
    "login_frequency",
    "behavior_score",
    "high_failed_login",
    "long_session"
]

X = df[feature_columns].copy()

# Fill missing values
X = X.fillna(0)

# -----------------------------
# Standardize
# -----------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, SCALER_PATH)

# -----------------------------
# Isolation Forest
# -----------------------------

model = IsolationForest(
    n_estimators=250,
    contamination=0.03,
    random_state=42,
    max_samples="auto"
)

model.fit(X_scaled)

# Save model
joblib.dump(model, MODEL_PATH)

# -----------------------------
# Predictions
# -----------------------------

prediction = model.predict(X_scaled)

# +1 = Normal
# -1 = Anomaly

df["if_prediction"] = prediction

# -----------------------------
# Decision score
# Higher = safer
# Lower = suspicious
# -----------------------------

decision = model.decision_function(X_scaled)

df["if_score"] = decision

# -----------------------------
# Convert into anomaly score
# -----------------------------

anomaly_score = -decision

# Normalize to 0-100

risk = (
    (anomaly_score - anomaly_score.min())
    /
    (anomaly_score.max() - anomaly_score.min())
) * 100

df["risk_score"] = risk.round(2)

# -----------------------------
# Risk Level
# -----------------------------

def risk_level(score):

    if score < 25:
        return "Low"

    elif score < 50:
        return "Medium"

    elif score < 75:
        return "High"

    return "Critical"


df["risk_level"] = df["risk_score"].apply(risk_level)

# -----------------------------
# Explainability
# -----------------------------

reason = []

for _, row in df.iterrows():

    reasons = []

    if row["high_failed_login"] == 1:
        reasons.append("High Failed Logins")

    if row["long_session"] == 1:
        reasons.append("Long Session")

    if row["device_trust_score"] < 50:
        reasons.append("Low Device Trust")

    if row["behavior_score"] > 2:
        reasons.append("Behavior Deviation")

    if row["login_frequency"] > 500:
        reasons.append("Abnormal Login Frequency")

    if len(reasons) == 0:
        reasons.append("Minor Behavioral Drift")

    reason.append(", ".join(reasons))

df["explanation"] = reason

# -----------------------------
# Save Results
# -----------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("Isolation Forest Training Completed")
print("=" * 60)

print("Rows :", len(df))
print("Anomalies :", (df["if_prediction"] == -1).sum())

print("\nRisk Distribution")
print(df["risk_level"].value_counts())

print("\nSaved model :", MODEL_PATH)
print("Saved scaler :", SCALER_PATH)
print("Results :", OUTPUT_FILE)