import datetime

from beanie.odm.operators.find.evaluation import RegEx

from models.db.package import Package, PackageTopLevelOnlyView
from models.db.release import Release
from models.db.release_analytics import ReleaseAnalytics


async def package_count() -> int:
    return await Package.count()


async def release_count() -> int:
    release_info = await ReleaseAnalytics.find_one()
    if release_info:
        return release_info.total_releases

    return 0


async def latest_packages(count: int) -> list[Package]:
    packages = await Package.find().sort("-last_updated").limit(count).to_list()
    return packages


def get_latest_release_for_package(package: Package) -> Release | None:
    if not package.releases:
        return None

    return max(package.releases, key=lambda r: (r.major_ver, r.minor_ver, r.build_ver))


async def get_package_by_id(package_name: str) -> Package | None:
    if not package_name:
        return None

    package_name = package_name.lower().strip()

    # package = await Package.get(package_name)
    package = await Package.find_one(Package.id == package_name)
    return package


async def packages_since(cutoff_date: datetime.datetime) -> list[PackageTopLevelOnlyView]:
    packages = await Package.find(Package.last_updated >= cutoff_date) \
        .sort('-last_updated') \
        .project(PackageTopLevelOnlyView) \
        .to_list()

    return packages


async def search(keyword) -> list[PackageTopLevelOnlyView]:
    if not keyword:
        return []
    keyword = keyword.lower().strip()

    packages = await Package.find(RegEx('_id', keyword)) \
        .project(PackageTopLevelOnlyView) \
        .sort('_id') \
        .to_list()

    return packages
