from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
import os

from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test_base_repo.db")
async_engine = create_async_engine(DATABASE_URL,
                                   future=True,
                                   pool_size=5,
                                   max_overflow=10,
                                   pool_timeout=30,
                                   pool_recycle=1800,
                                   echo=True,)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

class BaseRepository:
    """
    A base class for repository implementations.
    It expects an AsyncSession to be injected upon instantiation.
    Also provides static methods for database initialization and engine disposal.
    """
    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Provides access to the SQLAlchemy AsyncSession for the instance."""
        return self._session

    # --------------------------------------------------------------------------
    # Class-level/Static methods (for global DB operations)
    # --------------------------------------------------------------------------
    @staticmethod
    async def initialize_database():
        """
        Creates all database tables defined by ORM models inheriting from Base.
        This should typically be called once at application startup.
        It uses the `async_engine` and `Base` imported from your database connection setup.
        """
        if not async_engine or not Base:
            raise RuntimeError(
                "async_engine and Base must be configured and imported "
                "for initialize_database to work."
            )

        async with async_engine.begin() as conn:
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables initialized successfully via BaseRepository.initialize_database().")

    @staticmethod
    async def dispose_engine():
        """
        Closes the database engine's connection pool.
        This should be called during application shutdown for graceful resource release.
        """
        if not async_engine:
            raise RuntimeError(
                "async_engine must be configured for dispose_engine to work."
            )

        print("Disposing database engine...")
        await async_engine.dispose()
        print("Database engine disposed successfully via BaseRepository.dispose_engine().")
