from sqlalchemy.ext.asyncio import AsyncSession
from src.db.engine import async_session_maker
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.tasks.infrastructure.db.repo import PGTaskRepo


class PGTaskUnitOfWork(ITaskUnitOfWork):
    """
    PostgreSQL implementation of the task unit of work.

    Manages a database session and provides access to the task repository.
    Ensures that operations are executed within a transactional context.

    Attributes:
        session_factory (Callable): A factory to create new async database sessions.
        session (AsyncSession): The current active session.
        tasks (PGTaskRepo): Repository for task operations.
    """
    def __init__(self, session_factory=async_session_maker):
        """
        Initialize the unit of work with a session factory.

        :param session_factory: Callable that returns a new AsyncSession.
        """
        self.session_factory = session_factory

    async def __aenter__(self):
        """
        Enter the async context manager.

        Creates a new session and initializes the task repository.
        """
        self.session: AsyncSession = self.session_factory()
        self.tasks = PGTaskRepo(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        """
        Exit the async context manager.

        Performs rollback if needed and closes the session.
        """
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self):
        """
        Commit the current transaction.
        """
        await self.session.commit()

    async def rollback(self):
        """
        Rollback the current transaction.
        """
        await self.session.rollback()
