from src.users.domain.dtos import UserUpdateDTO
from src.users.domain.entities import User, UserUpdate
from src.users.domain.interfaces.password_hasher import IPasswordHasher
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


async def update_user(
    user_pk: int,
    user_data: UserUpdateDTO,
    pwd_hasher: IPasswordHasher,
    uow: IUserUnitOfWork,
) -> User:
    """
    Update an existing user's data.

    Applies the given update fields to the user with the specified primary key,
    saves the changes to the database, and commit the transaction.

    :param user_pk: Primary key of the user to update.
    :param user_data: Data Transfer Object with fields to update.
    :param uow: Unit Of Work instance for handling user repository operations.
    :return: Updated user entity object.
    """
    new_user_data = UserUpdate(
        id=user_pk,
        **{key: value for key, value in user_data.model_dump(mode="json").items() if key != "password" and value is not None},
        hashed_password=pwd_hasher.hash(user_data.password) if user_data.password else None
    )
    async with uow:
        user = await uow.users.update(new_user_data)
        await uow.commit()
    return user
