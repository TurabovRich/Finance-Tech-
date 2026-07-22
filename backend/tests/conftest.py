import asyncio
import sys
from pathlib import Path

# Ensure `app` package is importable when running pytest from backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = settings.TEST_DATABASE_URL or settings.DATABASE_URL.rsplit("/", 1)[0] + "/clarity_test"


@pytest.fixture(scope="session", autouse=True)
def _prepare_schema():
    """Recreate the test database schema once per test run, in its own throwaway
    event loop. Deliberately NOT a pytest-asyncio fixture: an asyncpg connection
    can't be reused across event loops, and mixing this session-scoped step with
    the function-scoped loop each test runs in caused exactly that ("cannot
    perform operation: another operation is in progress"). Keeping schema setup
    fully synchronous and self-contained avoids the whole class of bug.
    Never touches DATABASE_URL — only TEST_DATABASE_URL — so local dev data is
    never at risk."""

    async def _reset() -> None:
        engine = create_async_engine(TEST_DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    asyncio.run(_reset())


@pytest_asyncio.fixture
async def db_session():
    """One connection + transaction per test, rolled back afterwards for isolation.
    Engine is created fresh per test so it's always bound to the current test's
    event loop."""
    engine = create_async_engine(TEST_DATABASE_URL)
    session_local = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_local() as session:
        yield session
        await session.rollback()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
