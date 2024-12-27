from fastapi import APIRouter, Body

from exceptions.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    AllRoomsAreBookedHTTPException
from schemas.hotels import Hotel
from schemas.rooms import Room
from services.bookings import BookingsService
from services.hotels import HotelsService
from services.rooms import RoomService
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_request: BookingAddRequest = Body()
):
    """Создание бронирования номера"""
    try:
        room: Room = await RoomService(db).get_room(room_id=booking_request.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    hotel: Hotel = await HotelsService(db).delete_hotel(room.hotel_id)
    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_request.dict())

    try:
        booking = await BookingsService(db).create_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    all_bookings = await BookingsService(db).get_all_bookings()

    return {"bookings": all_bookings}


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    bookings = await BookingsService(db).get_my_bookings(user_id)
    return {"bookings": bookings}
