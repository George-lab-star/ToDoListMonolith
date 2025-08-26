from src.users.domain.interfaces.user_uow import IUserUnitOfWork


async def delete_user(
    user_pk: int,
    uow: IUserUnitOfWork,
) -> None:
    """
    Delete a user by primary key.

    This function delete a user from the database,
    using provided unit of work and commits the transaction.

    :param user_pk: Primary key of the user to be deleted.
    :param uow: Unit Of Work instance for handling user repository operations.
    """
    async with uow:
        await uow.users.delete(user_pk)
        await uow.commit()
