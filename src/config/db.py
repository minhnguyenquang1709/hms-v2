# TODO: add logging
import os
from typing import AsyncIterator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
    AsyncEngine,
    AsyncConnection,
)
from sqlalchemy.orm import DeclarativeBase, declarative_base
import contextlib # allow context management.
# context manager:
# - allows you to allocate and release resources precisely when you want to.
# - ensures resources are always closed at the end

load_dotenv()


# config
class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER", "fastapi"),
            DB_PASSWORD=os.getenv("DB_PASSWORD", "fastapi-password"),
            DB_HOST=os.getenv("DB_HOST", "fastapi-postgresql"),
            DB_PORT=os.getenv("DB_PORT", "5432"),
            DB_NAME=os.getenv("DB_NAME", "fastapi"),
        ),
    )


config = Config


class Base(AsyncAttrs, DeclarativeBase):
    pass


# abstracting the database connection and session handling
class DatabaseSessionManager:
    # create the object first (__init__), then configure it later with more details (init).
    def __init__(self):
        """
        Sets up default values or empty attributes.
        """
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None  # factory pattern

    def init(self, host_url: str):
        """
        Actually initializes the database connection and session factory.

        Args:
            host_url (str): the database connection URL.
        """
        self._engine = create_async_engine(
            url=host_url,
            echo=True,  # enable logging, use the python 'logging' module under the hood
            pool_size=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._engine,  # optional Engine or Connection. all SQL operations performed by this session will execute via this connectable
        )

    async def close(self):
        """
        Close database connection.
        """
        if self._engine is None:
            raise Exception("Database engine is not initialized.")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Context manager to get a database connection.

        Returns:
            AsyncIterator[AsyncConnection]: An asynchronous iterator that yields a database connection.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized.")

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                raise e