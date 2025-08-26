from src.users.domain.entities import UserCreate, User
from src.users.domain.interfaces.password_hasher import IPasswordHasher
from src.users.domain.interfaces.user_uow import IUserUnitOfWork
from src.users.domain.dtos import UserCreateDTO


async def register_user(
    user_data: UserCreateDTO,
    pwd_hasher: IPasswordHasher,
    uow: IUserUnitOfWork,
) -> User:
    """
    Register a new user in the system.

    This function hashes the password, creates a new user user entity,
    saves it to the database, and commites the transaction.

    :param user_data: Data Transfer Object containing user registration details.
    :param pwd_hasher: Password hasher.
    :param uow: Unit of Work instance for handling user reposittory operations.
    :return: New created user object.
    """
    new_user_data = UserCreate(
        **{key: value for key, value in user_data.model_dump(mode="json").items() if key != "password"},
        hashed_password=pwd_hasher.hash(user_data.password)
    )
    async with uow:
        new_user = await uow.users.add(new_user_data)
        await uow.commit()
    return new_user
