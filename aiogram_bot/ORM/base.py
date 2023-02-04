import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")

Engine = create_async_engine(DATABASE_URL, echo=True)
Session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=Engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def create_database():
    try:
        from .users import User
        # from .posts import Post, Media

        async with Engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except ImportError:
        raise


async def stop_database():
    await Engine.dispose()


if __name__ == '__main__':
    try:
        import asyncio

        asyncio.run(create_database())
    except ImportError:
        raise
