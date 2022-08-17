import asyncio
import datetime

import pymongo.errors

from models import mongo_setup
from models.package import Package
from services import package_service, user_service


async def main():
    await mongo_setup.init_db('pypi')

    print("--------------------------")
    print(" PyPI CLI ")
    print("--------------------------")
    print()

    pc = await package_service.package_count()
    rc = await package_service.release_count()
    print(f"We have {pc:,} packages with {rc:,} releases.")

    latest = await package_service.latest_packages(5)
    print("The latest 5 packages are:")
    for p in latest:
        r: "Release|None" = package_service.get_latest_release_for_package(p)
        if not r:
            print(f'* {p.id}')
        else:
            print(f'* {p.id:<10} with latest release on {r.created_date.isoformat().replace("T", " ")}')
    print()
    print("Boto package:")
    boto = await package_service.get_package_by_id('boto3')
    print(boto)

    print()
    # cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    t0 = datetime.datetime.now()
    cutoff = datetime.datetime(year=2022, month=5, day=10, hour=15)
    packages = await package_service.packages_since(cutoff)
    dt = datetime.datetime.now() - t0
    print(f"That took {dt.total_seconds() * 1000:,} ms")

    print(f"There are {len(packages)} recent packages.")
    # for p in packages:
    #     print(f'{p.id}: {p.summary}')
    print()

    print()
    print(f"We have {await user_service.user_count():,} users.")

    print("Let's create one more:")
    name = input("What's there name? ").strip()
    email = name.replace(' ', '-') + '@gmail.com'
    try:
        user = await user_service.create_account(name, email, "a")
    except pymongo.errors.DuplicateKeyError:
        print(f"Cannot create user, already exists with {email}.")

    print(f"Now we have {await user_service.user_count():,} users.")
    user = await user_service.get_user_by_email(email)
    print(f"We added {user}!")


if __name__ == '__main__':
    asyncio.run(main())
