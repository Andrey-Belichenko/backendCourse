from datetime import date

from src.schemas.hotels import HotelAdd
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2023, month=8, day=10),
        date_to=date(year=2024, month=8, day=15),
        price=100
    )

    new_booking_data = await db.bookings.add(booking_data)

    loaded_booking_data = (await db.bookings.get_all())[new_booking_data.id-1]

    assert new_booking_data == loaded_booking_data

    booking_data_to_modify = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2023, month=5, day=10),
        date_to=date(year=2024, month=5, day=15),
        price=150
    )

    await db.bookings.edit(booking_data_to_modify)

    modified_booking_data = (await db.bookings.get_all())[new_booking_data.id-1]

    assert modified_booking_data is not new_booking_data

    await db.bookings.delete(id=modified_booking_data.id)

    assert not await db.bookings.get_one_or_none()

    await db.commit()
