import pydantic


class ItemCountModel(pydantic.BaseModel):
    count: int
