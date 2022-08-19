import asyncio
import http

import fastapi
from starlette.requests import Request
from starlette.responses import JSONResponse

from models.api.create_user_model import CreateUserModel, CreateUserResponseModel
from services import user_service

router = fastapi.APIRouter(prefix='/api/users')


@router.post('/', status_code=http.HTTPStatus.CREATED, response_model=CreateUserResponseModel)
async def create_user(new_user: CreateUserModel):
    """
    Creates a new user...
    """
    # print(f"Processing {new_user}")
    user = await user_service.get_user_by_email(new_user.email)
    if user:
        model = CreateUserResponseModel(status='error', message=f'User exists with email {new_user.email}')
        return JSONResponse(content=model.dict(), status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY)

    user = await user_service.create_account(new_user.name, new_user.email, new_user.password.get_secret_value())
    return CreateUserResponseModel(id=str(user.id), message=f'Created new user.', location=f'/api/users/{user.id}')

# @router.route('/')
# def func(request: Request):
#     if request.method == 'GET':
#         ...
#     elif request.method == 'POST':
#         ...
#
#
# @router.get('/')
# def func_get():
#     ...
#
# @router.post('/')
# def func_post():
#     ...
