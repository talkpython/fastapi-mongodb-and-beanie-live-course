import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import package_api
from models.db import mongo_setup
from views import home

app = fastapi.FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(home.router, include_in_schema=False)
app.include_router(package_api.router)


# NO! -> asyncio.run(mongo_setup.init_db('pypi'))

@app.on_event("startup")
async def load_db():
    await mongo_setup.init_db('pypi')


uvicorn.run(app)
