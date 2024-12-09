from src.schemas.facilities import FacilitiesAdd


async def test_create_facilities(ac):
    response = await ac.post(url="/facilities", json={"title": "test facility name"})

    print(f"{response.json()=}")

    assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    print(f"{response.json()=}")

    assert response.status_code == 200


