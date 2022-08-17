import fastapi
import starlette.responses
from pydantic import ValidationError
import pymongo.errors

from models.api.item_count_model import ItemCountModel
from models.api.package_search_model import PackageSearchModel
from models.db.package import Package
from services import package_service

router = fastapi.APIRouter(prefix='/api/packages')


@router.get('/count', response_model=ItemCountModel)
async def count_packages():
    count = await package_service.package_count()
    model = ItemCountModel(count=count)
    return model


@router.get('/details/{package_name}', response_model=Package)
async def package_details(package_name: str):
    try:
        package = await package_service.get_package_by_id(package_name)
        if not package:
            return starlette.responses.Response(status_code=404)

        return package
    except ValidationError as ve:
        print("We ran into an error converting your data")
        return fastapi.Response(content=str(ve), status_code=500)
    except pymongo.errors.PyMongoError as pe:
        print("Trouble with the DB for now.")
        return fastapi.Response(content=str(pe), status_code=500)
    except Exception as e:
        print("General error")
        return fastapi.Response(content=str(e), status_code=500)


@router.get('/search/{keyword}', response_model=PackageSearchModel)
async def package_search(keyword: str):
    packages = await package_service.search(keyword)
    package_names = [p.id for p in packages]
    model = PackageSearchModel(keyword=keyword, packages=package_names)
    return model
