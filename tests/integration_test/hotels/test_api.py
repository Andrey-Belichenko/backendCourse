async def test_get_hotel(ac):
    response = await ac.get(
        "/hotels", params={"date_from": "2024-07-03", "date_to": "2024-07-13"}
    )

    assert response.status_code == 200
