import pydantic

from models.db.package import Package


class PackageSearchModel(pydantic.BaseModel):
    keyword: str
    packages: list[str]