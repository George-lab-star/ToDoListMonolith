from src.users.domain.entities import UserCreate, User, UserUpdate
from src.users.domain.exceptions import UserNotFound
from src.users.domain.interfaces.user_repo import IUserRepo
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


class FakeUserRepo(IUserRepo):
    """
    In-memory implementation of IUserRepo for testing purposes.
    Simulates user repository behavior without database persistence.
    """
    
    def __init__(self):
        """Initialize with empty user list and starting ID counter."""
        self._users = []
        self._last_user_id = 0

    async def add(self, user: UserCreate) -> User:
        """
        Add a new user to the repository.
        
        Args:
            user: UserCreate object containing user data
            
        Returns:
            User: The newly created user with assigned ID
        """
        new_user = User(id=self._get_new_user_id(), **user.dict)
        self._users.append(new_user)
        return new_user

    async def get_by_pk(self, pk: int, to_domain: bool = True) -> User:
        """
        Retrieve a user by their primary key (ID).
        
        Args:
            pk: ID of the user to retrieve
            
        Returns:
            User: The found user
            
        Raises:
            UserNotFound: If no user with the given ID exists
        """
        for user in self._users:
            if user.id == pk:
                return user

        raise UserNotFound(detail=f"User with id {pk} not found")

    async def get_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email address.
        
        Args:
            email: Email address of the user to retrieve
            
        Returns:
            User: The found user
            
        Raises:
            UserNotFound: If no user with the given email exists
        """
        for user in self._users:
            if user.email == email:
                return user

        raise UserNotFound(detail=f"User with email {email} not found")

    async def update(self, user_data: UserUpdate) -> User:
        """
        Update an existing user with new data.
        
        Args:
            user_data: UserUpdate object containing fields to update
            
        Returns:
            User: The updated user
        """
        user = await self.get_by_pk(user_data.id)

        for field, value in user_data.dict.items():
            if value is not None:
                setattr(user, field, value)

        return user

    async def delete(self, pk: int) -> None:
        """
        Delete a user by their primary key (ID).
        
        Args:
            pk: ID of the user to delete
            
        Raises:
            UserNotFound: If no user with the given ID exists
        """
        user = await self.get_by_pk(pk)
        self._users.remove(user)

    def _get_new_user_id(self) -> int:
        """
        Generate a new unique user ID.
        
        Returns:
            int: The next available user ID
        """
        self._last_user_id += 1
        return self._last_user_id


class FakeUserUnitOfWork(IUserUnitOfWork):
    """
    In-memory implementation of IUserUnitOfWork for testing.
    Manages transaction state for user operations.
    """
    
    users: IUserRepo

    def __init__(self):
        """Initialize with user repository and commit state."""
        self.users = FakeUserRepo()
        self.committed = False

    async def _commit(self):
        """
        Mark the current transaction as committed.
        Sets the committed flag to True.
        """
        self.committed = True

    async def rollback(self):
        """
        Rollback the current transaction.
        No-op in this in-memory implementation.
        """
        pass
