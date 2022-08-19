from typing import Literal

import pydantic


class CreateUserModel(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    password: pydantic.SecretStr = pydantic.Field()
    age: int

    class Config:
        schema_extra = {
            # ...
        }


class CreateUserResponseModel(pydantic.BaseModel):
    id: str | None
    location: str | None
    status: Literal['success', 'error'] = 'success'
    message: str = ''
