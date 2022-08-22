import beanie


class ReleaseAnalytics(beanie.Document):
    total_releases: int = 0

    class Settings:
        name = "release_analytics"
        indexes = []
