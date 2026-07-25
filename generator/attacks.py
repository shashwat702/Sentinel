import random

ATTACK_TYPES = [
    "normal",
    "brute_force",
    "impossible_travel",
    "credential_stuffing",
    "device_spoofing",
    "lateral_movement",
    "low_slow_exfiltration",
    "insider_drift"
]

ATTACK_PROBABILITY = 0.03   # 3%

def choose_attack():
    if random.random() < ATTACK_PROBABILITY:
        return random.choice(ATTACK_TYPES[1:])
    return "normal"