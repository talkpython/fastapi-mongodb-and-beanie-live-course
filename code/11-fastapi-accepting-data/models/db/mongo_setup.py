from typing import Optional

import beanie
import motor.motor_asyncio

from models.db.release_analytics import ReleaseAnalytics
from models.db.user import User
from models.db.package import Package


async def init_db(database: str, server: Optional[str] = 'localhost',
                  port: int = 27017, username: Optional[str] = None, password: Optional[str] = None,
                  use_ssl: bool = False):
    server = server or 'localhost'
    port = port or 27017

    await _motor_init(db=database, password=password, port=port, server=server,
                      use_ssl=use_ssl, username=username, models=[User, Package, ReleaseAnalytics])


async def _motor_init(db: str, password: Optional[str], port: int, server: str,
                      use_ssl: bool, username: Optional[str], models):
    conn_string = get_connection_string(password, port, server, use_ssl, username)
    print(f'Initializing motor connection for db {db} on {server}:{port}')
    print(f'Connection string: {conn_string.replace(password or "NO_PASSWORD", "***********")}')

    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)

    # Init beanie with the Product document class
    await beanie.init_beanie(database=client[db], document_models=models)
    print(f"Init done for db {db}")


def get_connection_string(password, port, server, use_ssl, username):
    if username or password:
        use_ssl = str(use_ssl).lower()
        return f"mongodb://{username}:{password}@{server}:{port}/?authSource=admin&tls={use_ssl}&tlsInsecure=true"
    else:
        return f"mongodb://{server}:{port}"
