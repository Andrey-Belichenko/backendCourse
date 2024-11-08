from fastapi import APIRouter, Body, HTTPException

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(db: DBDep,
                         user_id: UserIdDep,
                         booking_request: BookingAddRequest = Body()):
    """ Создание бронирования номера """
    room = await db.rooms.get_one_or_none(id=booking_request.room_id)
    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id,
                               price=room_price,
                               **booking_request.dict())

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"booking": booking}


@router.get("")
async def bookings(db: DBDep):

    all_bookings = await db.bookings.get_all()

    return {"bookings": all_bookings}


@router.get("/me")
async def my_bookings(db: DBDep,
                      user_id: UserIdDep,):
    _bookings = await db.bookings.get_filtered(user_id=user_id)

    return {"bookings": _bookings}
