from fastapi import APIRouter, Body

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_request: BookingAddRequest = Body()
):
    """Создание бронирования номера"""
    room = await db.rooms.get_one_or_none(id=booking_request.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)

    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_request.dict())

    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)

    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    all_bookings = await db.bookings.get_all()

    return {"bookings": all_bookings}


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    _bookings = await db.bookings.get_filtered(user_id=user_id)

    return {"bookings": _bookings}
