import beanie
import motor.motor_asyncio

from models.release_analytics import ReleaseAnalytics
from models.user import User
from models.package import Package


async def init_db(database: str):
    conn_str = 'mongodb://localhost:27017'
    db_client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(db_client[database], document_models=[User, Package, ReleaseAnalytics])
