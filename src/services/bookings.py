from src.exceptions.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingsService(BaseService):
    async def get_all_bookings(self):
        all_bookings = await self.db.bookings.get_all()

        return all_bookings

    async def get_my_bookings(self, user_id):
        _bookings = await self.db.bookings.get_filtered(user_id=user_id)

        return _bookings

    async def create_booking(self, user_id: int, booking_data: BookingAddRequest):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex

        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price

        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.dict(),
        )

        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)

        await self.db.commit()
        return booking

