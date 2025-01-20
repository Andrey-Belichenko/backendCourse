from fastapi import APIRouter, Body

from src.exceptions.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.services.bookings import BookingsService
from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_request: BookingAddRequest = Body()
):
    """Создание бронирования номера"""
    try:
        booking = await BookingsService(db).create_booking(user_id, booking_request)
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
