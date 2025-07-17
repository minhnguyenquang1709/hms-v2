import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_TYPE = "postgresql"
DB_DRIVER = "psycopg"
DB_SEPARATOR = "+" if DB_DRIVER else ""

# create engine
DATABASE_URL = f"{DB_TYPE}{DB_SEPARATOR}{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Base(AsyncAttrs, DeclarativeBase):
  pass

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,  # enable logging, use the python 'logging' module under the hood
    pool_size=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# async session factory (factory pattern)
async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)