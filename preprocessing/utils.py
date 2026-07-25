from math import radians, sin, cos, sqrt, atan2

# Approximate coordinates for demo purposes
CITY_COORDS = {
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Delhi": (28.6139, 77.2090),
    "Phoenix": (33.4484, -112.0740),
    "Atlanta": (33.7490, -84.3880),
    "Chicago": (41.8781, -87.6298),
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1351, 11.5820),
    "Singapore": (1.3521, 103.8198)
}


def haversine(city1, city2):
    if city1 not in CITY_COORDS or city2 not in CITY_COORDS:
        return 0

    lat1, lon1 = CITY_COORDS[city1]
    lat2, lon2 = CITY_COORDS[city2]

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c