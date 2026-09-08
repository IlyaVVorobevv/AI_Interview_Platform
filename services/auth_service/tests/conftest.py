from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy import select

import pytest_asyncio

from app.main import app
from app.models.user import User
from app.database.session import get_db
from app.database.base import Base
from app.database.config import settings


TEST_DATABASE_URL = settings.test_database_url

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="function")
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


transport = ASGITransport(app=app)
@pytest_asyncio.fixture
async def client(setup_db):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture()
async def db_session(setup_db):
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture()
async def create_user_helper(setup_db, client):
    async def _create_user(email, username, password):
        build_json = {"email": email, "username": username, "password": password}
        response = await client.post("/auth/register", json=build_json)
        return response
    return _create_user

@pytest_asyncio.fixture()
async def get_user_helper(setup_db, db_session):
    async def _get_user(email):
        query = select(User).where(User.email == email)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()
    return _get_user