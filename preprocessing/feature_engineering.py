from pathlib import Path

import pandas as pd

from utils import haversine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_logs.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_logs.csv"

df = pd.read_csv(RAW_DATA_PATH)

# -----------------------------
# Timestamp Features
# -----------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["login_hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
df["month"] = df["timestamp"].dt.month
df["is_weekend"] = df["day_of_week"] >= 5

# -----------------------------
# Failed Login Indicator
# -----------------------------

df["high_failed_login"] = (
    df["failed_attempts"] > 10
).astype(int)

# -----------------------------
# Long Session Indicator
# -----------------------------

df["long_session"] = (
    df["session_duration"] > 120
).astype(int)

# -----------------------------
# Resource Sensitivity
# -----------------------------

resource_scores = {

    "/dashboard": 1,
    "/profile": 1,
    "/notifications": 1,

    "/employee": 2,
    "/leave": 2,
    "/crm": 2,

    "/finance": 4,
    "/accounts": 4,
    "/invoice": 4,

    "/admin": 5,
    "/security": 5,
    "/vpn": 5,
    "/logs": 5,
    "/database": 5,
    "/server": 5
}

df["resource_sensitivity"] = (
    df["resource_accessed"]
      .map(resource_scores)
      .fillna(3)
)

# -----------------------------
# Device Trust
# -----------------------------

trusted = [
    "Windows Laptop",
    "MacBook",
    "Linux Workstation"
]

df["device_trust_score"] = df["device"].apply(
    lambda x: 100 if x in trusted else 40
)

# -----------------------------
# Login Frequency
# -----------------------------

login_freq = (
    df.groupby("entity_id")
      .size()
      .rename("login_frequency")
)

df = df.merge(
    login_freq,
    on="entity_id"
)

# Save

PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(
    PROCESSED_DATA_PATH,
    index=False
)

print(df.head())

print()

print("Processed dataset saved.")
