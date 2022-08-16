import datetime
from typing import Optional

import beanie
import pydantic
import pymongo
from beanie import PydanticObjectId

from models.release import Release


class Package(beanie.Document):
    id: str = pydantic.Field(unique=True)
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    summary: str
    description: Optional[str] = None

    home_page: Optional[str] = None
    docs_url: Optional[str] = None
    package_url: Optional[str] = None

    author_name: Optional[str] = None
    author_email: Optional[str] = None

    license: Optional[str] = None

    releases: list[Release] = []
    maintainer_ids: list[PydanticObjectId] = []

    class Collection:
        name = "packages"
        indexes = [
            pymongo.IndexModel(keys=[("created_date", pymongo.DESCENDING)], name="created_date_descend"),
            pymongo.IndexModel(keys=[("last_updated", pymongo.DESCENDING)], name="last_updated_descend"),
            pymongo.IndexModel(keys=[("author_email", pymongo.ASCENDING)], name="author_email_ascending"),
            pymongo.IndexModel(keys=[("license", pymongo.ASCENDING)], name="license_ascending"),
            pymongo.IndexModel(keys=[("maintainer_ids", pymongo.ASCENDING)], name="maintainer_ids_ascend"),

            pymongo.IndexModel(
                [
                    ("releases.major_ver", pymongo.DESCENDING),
                    ("releases.minor_ver", pymongo.DESCENDING),
                    ("releases.build_ver", pymongo.DESCENDING),
                ],
                name="release_versions_descend",
            )
        ]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'<Package {self.id} ({len(self.releases):} releases)>'


class PackageTopLevelOnlyView(pydantic.BaseModel):
    id: Optional[str]
    summary: str

    class Settings:
        projection = {
            "id": "$_id",
            "summary": "$summary"
        }
