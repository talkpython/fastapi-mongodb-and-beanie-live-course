import datetime
from typing import Optional

import pydantic


class Release(pydantic.BaseModel):
    major_ver: int
    minor_ver: int
    build_ver: int

    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    comment: Optional[str] = None
    url: Optional[str] = None
    size: int = 0

    @property
    def version_text(self):
        return '{}.{}.{}'.format(self.major_ver, self.minor_ver, self.build_ver)
