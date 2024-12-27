from services.base import BaseService


class BookingsService(BaseService):
    async def get_all_bookings(self):
        all_bookings = await self.db.bookings.get_all()

        return all_bookings

    async def get_my_bookings(self, user_id):
        _bookings = await self.db.bookings.get_filtered(user_id=user_id)

        return _bookings

    async def create_booking(self, _booking_data, hotel_id):
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel_id)
        await self.db.commit()

        return booking

