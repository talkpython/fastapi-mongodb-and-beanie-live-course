import datetime

import beanie
import pydantic
import pymongo


class CalculatorResult(beanie.Document):
    id: beanie.PydanticObjectId | None = pydantic.Field(alias='request_id')
    x: int
    y: int
    created: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    action: str
    result: float

    class Collection:
        name = "calculations"
        indexes = [
            pymongo.IndexModel(keys=[("created", pymongo.DESCENDING)], name="created_descend"),
        ]
