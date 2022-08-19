import uvicorn
import fastapi

from models.db import mongo_setup
from models.db.calculator_result import CalculatorResult
from services import calc_service

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    await mongo_setup.init_db('calculator')


@app.get('/', include_in_schema=False)
def home():
    return fastapi.Response(content=
                            "<h1>FastAPI Course Homework</h1>"
                            "Click this to start: <br>"
                            "<a href='/api/calculator/add/7/11'>/api/calculator/add/7/11</a>")


@app.get('/api/calculator/add/{x}/{y}', response_model=CalculatorResult)
async def add(x: int, y: int):
    model = await calc_service.record_calculation(x, y, "add", x + y)
    return model


if __name__ == '__main__':
    uvicorn.run(app)
