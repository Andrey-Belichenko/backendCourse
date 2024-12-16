import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("user_email, user_password", [
                        ("user1@test.com", "test_password"),
                        ("user2@test.com", "тест пароль"),
                        ("user3@test.com", ""),
                        ("a@a.com", ""),
                        ])
async def test_create_user(user_email, user_password,
                           ac):
    response = await ac.post(
        "/auth/register",
        json={"email": user_email,
              "password": user_password}
    )

    assert response.status_code == 200


@pytest.mark.parametrize("user_email, user_password", [
                        ("user1@test.com", "test_password"),
                        ("user2@test.com", "тест пароль"),
                        ("user3@test.com", ""),
                        ])
async def test_login_user(user_email, user_password,
                          ac):
    access_token = await ac.post("/auth/login",
                                 json={"email": user_email,
                                       "password": user_password}
                                 )

    assert access_token.json()["access_token"] is not None
    assert ac.cookies["access_token"]


@pytest.mark.parametrize("user_email, user_password", [
                        ("user1@test.com", "test_password"),
                        ])
async def test_login_and_logout(user_email, user_password,
                                ac):

    access_token = await ac.post("/auth/login",
                                 json={"email": user_email,
                                       "password": user_password}
                                 )

    assert access_token.json()["access_token"] is not None
    assert ac.cookies["access_token"]

    assert ac.cookies["access_token"]

    print(f"{ac.cookies=}")

    response = await ac.get("/auth/me")

    assert response.status_code == 200
    assert response.json()

    response = await ac.post("/auth/logout")

    assert response.status_code == 200
    assert not ac.cookies

    response = await ac.get("/auth/me")

    assert response.status_code == 401
    assert response.json()['detail'] == 'Вы не предоставили токен доступа'
