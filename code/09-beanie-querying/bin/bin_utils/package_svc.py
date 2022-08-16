from models.package import Package
from models.release_analytics import ReleaseAnalytics


async def release_count() -> int:
    release_info = await ReleaseAnalytics.find_one()
    if not release_info:
        release_info = ReleaseAnalytics()
        await release_info.save()

    return release_info.total_releases


async def package_count() -> int:
    return await Package.count()


async def increment_release_count(num: int):
    release_info = await ReleaseAnalytics.find_one()
    if not release_info:
        release_info = ReleaseAnalytics()

    release_info.total_releases += num
    await release_info.save()


async def reset_release_count():
    release_info = await ReleaseAnalytics.find_one()
    if not release_info:
        release_info = ReleaseAnalytics()

    release_info.total_releases = 0
    await release_info.save()
