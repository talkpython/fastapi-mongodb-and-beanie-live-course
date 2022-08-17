import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/', include_in_schema=False)
async def index(request: Request):
    db_data = {'title': 'FastAPI PyPI api'}  # <-- pydantic.dict()
    return templates.TemplateResponse('index.html', {"request": request} | db_data)
