import datetime
from typing import Optional

import beanie
import pydantic
import pymongo


class User(beanie.Document):
    name: str
    email: pydantic.EmailStr
    hash_password: Optional[str]

    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_login: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    profile_image_url: Optional[str] = None

    class Collection:
        name = "users"
        indexes = [
            pymongo.IndexModel(keys=[("email", pymongo.ASCENDING)], name="email_ascend", unique=True),
            pymongo.IndexModel(keys=[("created_date", pymongo.ASCENDING)], name="created_date_ascend"),
            pymongo.IndexModel(keys=[("last_login", pymongo.ASCENDING)], name="last_login_ascend"),
        ]
