# ruff: noqa: E402
import json

import pytest

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependencies import get_db
from src.config import settings
from src.database import BaseORM, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)

    with open("tests/mocks/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)

    with open("tests/mocks/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register", json={"email": "user@auto.com", "password": "test_password"}
    )


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(register_user, ac) -> AsyncClient:
    access_token = await ac.post(
        "/auth/login", json={"email": "user@auto.com", "password": "test_password"}
    )

    assert access_token.json()["access_token"] is not None
    assert ac.cookies["access_token"]

    yield ac
