import json

import pytest

from src.config import settings
from src.database import BaseORM, engine_null_pool
from src.main import app
from src.models import *
from httpx import AsyncClient

from src.schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={"email": "user@auto.com",
                  "password": "test_password"}
            )


@pytest.fixture(scope="session", autouse=True)
async def mock_hotel_add(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/mocks/mock_hotels.json", 'r', encoding='utf-8') as mock:
            hotels_to_add = json.load(mock)
            for hotel_data in hotels_to_add:
                response = await ac.post(url="/hotels", json=hotel_data)


@pytest.fixture(scope="session", autouse=True)
async def mock_room_add(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/mocks/mock_rooms.json", 'r', encoding='utf-8') as mock:
            rooms_to_add = json.load(mock)
            for room_data in rooms_to_add:
                hotel_id = room_data["hotel_id"]
                response = await ac.post(url=f"/hotels/{hotel_id}/rooms", json=room_data)
                print(f"{response=}")
