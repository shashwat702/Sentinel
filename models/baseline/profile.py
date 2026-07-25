import pandas as pd


class UserProfile:

    def __init__(self, entity_id):

        self.entity_id = entity_id

        self.avg_login_hour = None

        self.std_login_hour = None

        self.common_devices = []

        self.common_countries = []

        self.common_resources = []

        self.avg_session = None


def build_profiles(df):

    profiles = {}

    grouped = df.groupby("entity_id")

    for entity, group in grouped:

        profile = UserProfile(entity)

        profile.avg_login_hour = group["login_hour"].mean()

        profile.std_login_hour = group["login_hour"].std()

        profile.avg_session = group["session_duration"].mean()

        profile.common_devices = list(
            group["device"].value_counts().head(3).index
        )

        profile.common_countries = list(
            group["country"].value_counts().head(3).index
        )

        profile.common_resources = list(
            group["resource_accessed"].value_counts().head(5).index
        )

        profiles[entity] = profile

    return profiles