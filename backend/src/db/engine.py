from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.config import settings

async_engine = create_async_engine(settings.database_url)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)