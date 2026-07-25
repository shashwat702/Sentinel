import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

DATA = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "isolation_results.csv"
)

MODEL = os.path.join(
    BASE_DIR,
    "saved_models",
    "attack_classifier.pkl"
)

OUTPUT = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_predictions.csv"
)

df = pd.read_csv(DATA)

model = joblib.load(MODEL)

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

pred = model.predict(X)
prob = model.predict_proba(X)

confidence = np.max(prob, axis=1)

df["predicted_attack"] = pred

df["prediction_confidence"] = confidence

# ------------------------------------
# Hybrid Risk
# ------------------------------------

risk = (
    0.35 * df["risk_score"] +
    0.35 * (df["behavior_score"] * 20) +
    0.30 * (confidence * 100)
)

risk = risk.clip(0, 100)

df["final_risk_score"] = risk.round(2)

# ------------------------------------
# Severity
# ------------------------------------

def severity(x):

    if x < 25:
        return "LOW"

    elif x < 50:
        return "MEDIUM"

    elif x < 75:
        return "HIGH"

    return "CRITICAL"

df["severity"] = df["final_risk_score"].apply(severity)

# ------------------------------------
# Recommendation
# ------------------------------------

def recommendation(row):

    attack = row["predicted_attack"]

    if attack == "normal":
        return "Allow Login"

    if attack == "brute_force":
        return "Lock Account + CAPTCHA"

    if attack == "credential_stuffing":
        return "Reset Password + MFA"

    if attack == "impossible_travel":
        return "Verify User Location"

    if attack == "device_spoofing":
        return "Block Device"

    if attack == "lateral_movement":
        return "Isolate Endpoint"

    if attack == "low_and_slow":
        return "SOC Investigation"

    if attack == "insider_drift":
        return "Monitor User"

    return "SOC Investigation"

df["recommended_action"] = df.apply(
    recommendation,
    axis=1
)

# ------------------------------------
# Save
# ------------------------------------

df.to_csv(
    OUTPUT,
    index=False
)

print("="*60)
print("Hybrid Risk Engine Completed")
print("="*60)

print(df[[
    "predicted_attack",
    "prediction_confidence",
    "final_risk_score",
    "severity",
    "recommended_action"
]].head())