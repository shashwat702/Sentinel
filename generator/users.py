import random

from departments import DEPARTMENTS
from config import AUTH_METHODS
from devices import DEVICES, BROWSERS
from locations import LOCATIONS


def generate_users(num_users=500):

    users = []

    department_names = list(DEPARTMENTS.keys())
    country_names = list(LOCATIONS.keys())

    for i in range(1, num_users + 1):

        department = random.choice(department_names)

        country = random.choice(country_names)

        city = random.choice(LOCATIONS[country])

        login_hour = random.randint(8, 10)

        logout_hour = random.randint(17, 19)

        session_mean = random.randint(15, 45)

        preferred_resources = random.sample(
            DEPARTMENTS[department],
            k=min(2, len(DEPARTMENTS[department]))
        )

        user = {

            "entity_id": f"USER_{i:04d}",

            "department": department,

            "country": country,

            "city": city,

            "device": random.choice(DEVICES),

            "browser": random.choice(BROWSERS),

            "preferred_auth": random.choice(AUTH_METHODS),

            "login_hour": login_hour,

            "logout_hour": logout_hour,

            "session_mean": session_mean,

            "preferred_resources": preferred_resources,

            "known_ips": [
                f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                for _ in range(3)
            ]
        }

        users.append(user)

    return users


if __name__ == "__main__":

    users = generate_users(5)

    for user in users:
        print(user)
