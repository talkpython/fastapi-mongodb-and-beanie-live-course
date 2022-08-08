import json
from pathlib import Path
from typing import Any, List

import pydantic as pydantic
from pydantic import BaseModel

data = {
    "description": "few clouds",
    "Category": "Clouds",
    "temp": '73.22',
}


class Forecast(pydantic.BaseModel):
    description: str | None
    category: str = pydantic.Field(alias='Category')
    temp: float


f = Forecast(**data)
# f = Forecast(description=data['description'], category=data['category'], ...)

print(f.json())


class Downloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class ProjectUrls(BaseModel):
    Homepage: str


class Info(BaseModel):
    author: str
    author_email: str
    bugtrack_url: Any
    synk: str
    quality_score: str
    days_since_release: int
    classifiers: List[str]
    description: str
    description_content_type: str
    docs_url: Any
    download_url: str
    downloads: Downloads
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: str
    project_url: str
    project_urls: ProjectUrls
    release_url: str
    requires_dist: List[str]
    requires_python: str
    summary: str
    version: str
    yanked: bool
    yanked_reason: Any


class Digests(BaseModel):
    md5: str
    sha256: str


class Release(BaseModel):
    version: str
    comment_text: str
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: Any
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: Any


class PackageModel(BaseModel):
    info: Info
    last_serial: int
    releases: List[Release]
    vulnerabilities: List


file = Path(__file__).parent / 'pydantic.json'
with open(file, 'r', encoding='utf-8') as fin:
    data = json.load(fin)

package = PackageModel(**data)
print(package)


print("Details about pydantic")
print(f"Name: {package.info.name}")
print(f"Releases: {len(package.releases)}")
