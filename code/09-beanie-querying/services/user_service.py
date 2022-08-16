from models.user import User


async def user_count() -> int:
    return await User.count()


async def create_account(name: str, email: str, password: str) -> User:
    user = User(name=name, email=email.lower().strip())
    await user.save()
    return user


async def get_user_by_email(email: str) -> User | None:
    return await User.find_one(User.email == email.lower().strip())
