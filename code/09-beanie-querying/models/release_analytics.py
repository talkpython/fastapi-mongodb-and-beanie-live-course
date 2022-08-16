import beanie


class ReleaseAnalytics(beanie.Document):
    total_releases: int = 0

    class Collection:
        name = "release_analytics"
        indexes = []
