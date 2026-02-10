from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        for stmt in [
            "ALTER TABLE resources ADD COLUMN folder VARCHAR",
            "ALTER TABLE resources RENAME COLUMN type TO category",
            "ALTER TABLE resources RENAME COLUMN url TO filename",
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_resources_filename ON resources(filename)",
            "ALTER TABLE resources ADD COLUMN deleted_at DATETIME",
            "ALTER TABLE resources ADD COLUMN thumbnail VARCHAR",
        ]:
            try:
                await conn.execute(text(stmt))
            except Exception:
                pass
    yield
    await engine.dispose()
