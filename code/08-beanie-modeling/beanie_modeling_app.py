import asyncio

from models import mongo_setup
from models.user import User


async def main():
    await mongo_setup.init_db('pypi')

    u = User(name="Michael", email="michael@talkpython.fm")
    print(f"We created: {u}")

    mk = await User.find_one(User.email == 'michael@talkpython.fm')
    if not mk:
        print("No MK, creating!")
        await u.save()
    else:
        print("MK already exists.")


if __name__ == '__main__':
    asyncio.run(main())
