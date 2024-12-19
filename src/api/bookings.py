from fastapi import APIRouter, Body, HTTPException

from exceptions.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from schemas.hotels import Hotel
from schemas.rooms import Room
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_request: BookingAddRequest = Body()
):
    """Создание бронирования номера"""
    try:
        room: Room = await db.rooms.get_one(id=booking_request.room_id)

    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=400, detail="Номер не найден")

    if not room:
        raise HTTPException(status_code=401, detail="Номер не найден")

    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_request.dict())

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

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
