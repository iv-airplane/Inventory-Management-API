import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app
from app.models.user import Role, User

engine = create_async_engine(
    "sqlite+aiosqlite:///",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = async_sessionmaker(engine, expire_on_commit=False)


async def get_test_db():
    async with TestSession() as db:
        yield db

# pytest.fixture is a setup for tests

@pytest.fixture
def auth_headers(client: TestClient) -> dict:
    client.post("/auth/register", json={"email":
  "u@u.com", "password": "pw12345"})
    token = client.post("/auth/login", data={"username": "u@u.com", "password": "pw12345"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client: TestClient) -> dict:
    """Registers a user via the normal API, then promotes it to admin
    directly in the DB -- there's no API-level way to create an admin."""
    client.post("/auth/register", json={"email": "admin@a.com", "password": "pw12345"})

    async def promote_to_admin():
        async with TestSession() as db:
            await db.execute(update(User).where(User.email == "admin@a.com").values(role=Role.admin))
            await db.commit()

    asyncio.run(promote_to_admin())

    token = client.post(
        "/auth/login", data={"username": "admin@a.com", "password": "pw12345"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client():
    """Fresh in-memory database and TestClient for each test."""
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(create_tables())
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as c:
        yield c

    # remove tables when done
    app.dependency_overrides.clear()
    asyncio.run(drop_tables())
