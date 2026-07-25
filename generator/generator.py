import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

from users import generate_users
from attacks import choose_attack
from departments import DEPARTMENTS
from locations import LOCATIONS

fake = Faker()

NUM_LOGS = 100000

users = generate_users(500)

logs = []

start_date = datetime(2025,1,1)

for _ in range(NUM_LOGS):

    user = random.choice(users)

    attack = choose_attack()

    ##################################################

    day_offset = random.randint(0,364)

    hour = int(random.gauss(user["login_hour"],1.5))

    hour = max(0,min(23,hour))

    minute = random.randint(0,59)

    timestamp = start_date + timedelta(
        days=day_offset,
        hours=hour,
        minutes=minute
    )

    ##################################################

    country = user["country"]

    city = user["city"]

    ip = random.choice(user["known_ips"])

    device = user["device"]

    browser = user["browser"]

    auth = user["preferred_auth"]

    session = max(
        1,
        int(random.gauss(user["session_mean"],5))
    )

    resource = random.choice(
        user["preferred_resources"]
    )

    success = True

    failed_attempts = 0

    ##################################################
    # Attack Injection
    ##################################################

    if attack=="brute_force":

        success=False

        failed_attempts=random.randint(15,50)

        auth="Password"

        session=1

    elif attack=="credential_stuffing":

        success=random.choice([False,False,False,True])

        failed_attempts=random.randint(20,80)

        auth="Password"

    elif attack=="impossible_travel":

        other_country=random.choice(
            [c for c in LOCATIONS if c!=country]
        )

        country=other_country

        city=random.choice(LOCATIONS[other_country])

    elif attack=="device_spoofing":

        device=random.choice([
            "Unknown Laptop",
            "Android",
            "MacBook",
            "Linux Workstation"
        ])

        browser=random.choice([
            "Tor",
            "Firefox",
            "Unknown"
        ])

    elif attack=="lateral_movement":

        resource="/admin"

    elif attack=="low_slow_exfiltration":

        timestamp=timestamp.replace(hour=3)

        session=random.randint(180,600)

        resource="/database"

    elif attack=="insider_drift":

        resource="/security"

        session=random.randint(60,180)

    ##################################################

    logs.append({

        "entity_id":user["entity_id"],

        "department":user["department"],

        "timestamp":timestamp,

        "country":country,

        "city":city,

        "source_ip":ip,

        "device":device,

        "browser":browser,

        "auth_method":auth,

        "resource_accessed":resource,

        "session_duration":session,

        "success":success,

        "failed_attempts":failed_attempts,

        "label":attack

    })

df=pd.DataFrame(logs)

output_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "synthetic_logs.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(
    output_path,
    index=False
)

print(df.head())

print()

print(df["label"].value_counts())

print()

print("Dataset Generated Successfully")
