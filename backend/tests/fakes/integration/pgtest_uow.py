import redis.asyncio as aioredis
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.auth.infrastructure.redis_refresh_repo import RedisRefreshTokenRepository
from src.tasks.infrastructure.db.unit_of_work import PGTaskUnitOfWork
from src.users.infrastructure.db.unit_of_work import PGUserUnitOfWork
from src.core.config import settings


async_engine = create_async_engine(settings.test_database_url, poolclass=NullPool)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class TestPGUserUnitOfWork(PGUserUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        """
        Initialize the test unit of work with a session factory.

        :param session_factory: Callable that returns a new AsyncSession.
        """
        self.session_factory = session_factory


class TestPGTaskUnitOfWork(PGTaskUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        """
        Initialize the test unit of work with a session factory.

        :param session_factory: Callable that returns a new AsyncSession.
        """
        self.session_factory = session_factory


class TestRedisRefreshTokenRepository(RedisRefreshTokenRepository):
    def __init__(self):
        self.redis_client = aioredis.from_url(
            url=settings.test_redis_url,
            decode_responses=True,
            encoding="utf-8"
        )
