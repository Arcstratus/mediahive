from collections.abc import AsyncGenerator

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"  # in-memory

engine_test = create_async_engine(TEST_DATABASE_URL)
async_session_test = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_test() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_database():
    """Create all tables before each test and drop them after."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession]:
    """Provide a transactional test database session."""
    async with async_session_test() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient]:
    """Provide an async HTTP client wired to the FastAPI app."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
