from pathlib import Path

import pandas as pd

from profile import build_profiles
from utils import z_score


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_logs.csv"
BASELINE_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "baseline_logs.csv"

df = pd.read_csv(PROCESSED_DATA_PATH)

profiles = build_profiles(df)

##########################################################

behavior_scores = []

for _, row in df.iterrows():

    profile = profiles[row["entity_id"]]

    score = 0

    ##################################################

    login_deviation = z_score(

        row["login_hour"],

        profile.avg_login_hour,

        profile.std_login_hour

    )

    score += login_deviation

    ##################################################

    if row["device"] not in profile.common_devices:

        score += 3

    ##################################################

    if row["country"] not in profile.common_countries:

        score += 4

    ##################################################

    if row["resource_accessed"] not in profile.common_resources:

        score += 2

    ##################################################

    session_diff = abs(

        row["session_duration"]

        - profile.avg_session

    ) / max(profile.avg_session, 1)

    score += session_diff

    behavior_scores.append(score)

##########################################################

df["behavior_score"] = behavior_scores

##########################################################

BASELINE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(

    BASELINE_DATA_PATH,

    index=False

)

print(df.head())

print()

print("Behavior baseline completed.")
