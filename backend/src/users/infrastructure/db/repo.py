from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.entities import User, UserCreate, UserUpdate
from src.users.domain.exceptions import UserAlreadyExists, UserNotFound
from src.users.domain.interfaces.user_repo import IUserRepo
from src.users.infrastructure.db.orm import DBUser


class PGUserRepo(IUserRepo):
    """
    PostgreSQL implementation of the user repository interface.

    This class handles CRUD operations for users using SQLAlchemy and a PostgreSQL database.

    Attributes:
        session (AsyncSession): The database session used for all operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository with an active database session.

        :param session: Async SQLAlchemy session.
        """
        super().__init__()
        self.session = session

    async def add(self, user: UserCreate) -> User:
        """
        Create a new user in the database.

        Attempts to persist a new user entity and flushes the session.
        Raises a custom exception if a uniqueness constraint is violated.

        :param user: Domain model representing the user to be created.
        :return: The created user as a domain model.
        :raises UserAlreadyExists: if a user with the same unique fields already exists.
        """
        obj = DBUser(**user.dict)
        self.session.add(obj)

        try:
            await self.session.flush()
        except IntegrityError as e:
            try:
                detail = "User can't be created. " + str(e.orig).split('\nDETAIL:  ')[1]
            except IndexError:
                detail = "User can't be created due to integrity error."
            raise UserAlreadyExists(detail=detail)

        return self._to_domain(obj)
    
    async def get_by_pk(self, pk: int, to_domain: bool = True) -> User | DBUser:
        """
        Return a user by primary key (ID).

        :param pk: User ID.
        :return: The retrieved user as a domain model.
        :raises UserNotFound: If no user with the given ID exists.
        """
        obj: DBUser | None = await self.session.get(DBUser, pk)
        if not obj:
            raise UserNotFound(detail=f"User with id {pk} not found")
        
        if to_domain:
            return self._to_domain(obj)
        return obj
    
    async def get_by_email(self, email: str) -> User:
        """
        Retrieve a user by email address.

        :param email: User email.
        :return: The retrieved user as a domain model.
        :raises UserNotFound: If no user with the given eamil exists.
        """
        stmt = select(DBUser).where(DBUser.email == email)
        result = await self.session.execute(stmt)
        obj: DBUser | None = result.scalar_one_or_none()

        if not obj:
            raise UserNotFound(detail=f"User with email {email} not found")

        return self._to_domain(obj)
    
    async def update(self, user_data: UserUpdate) -> User:
        """
        Update user fields based on input data.

        :param user_data: Domain model containing updated user fields.
        :return: Updated user as a domain model.
        :raises UserNotFound: If the user with the specified ID does not exist.
        """
        stmt = select(DBUser).where(DBUser.id == user_data.id)
        result = await self.session.execute(stmt)
        obj: DBUser | None = result.scalar_one_or_none()

        if not obj:
            raise UserNotFound(detail=f"User with id {user_data.id} not found")

        for field, value in user_data.dict.items():
            if value != None:
                setattr(obj, field, value)

        await self.session.flush()

        return self._to_domain(obj)

    async def delete(self, pk: int) -> None:
        """
        Delete a user by primary key (ID).

        :param pk: ID of the user to delete.
        :raises UserNotFound: If the user with the given ID does not exist.
        """
        obj = await self.session.get(DBUser, pk)
        if not obj:
            raise UserNotFound(detail=f"User with id {pk} not found")

        await self.session.delete(obj)


    @staticmethod
    def _to_domain(obj: DBUser) -> User:
        return User(
            id=obj.id,
            name=obj.name,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
            is_superuser=obj.is_superuser,
            is_verified=obj.is_verified
        )