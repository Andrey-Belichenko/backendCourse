from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.utils.CustomExceptions import UnableRoomBookingException


class BookingsRepository(BaseRepository):
    model = BookingsORM

    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, _booking_data):

        query = rooms_ids_for_booking(_booking_data.date_from,
                                      _booking_data.date_to)

        result = await self.session.execute(query)

        vacant_rooms_ids_list = result.scalars().all()

        if _booking_data.room_id not in vacant_rooms_ids_list:
            raise UnableRoomBookingException(406, _booking_data.room_id)

        return await self.add(_booking_data)
