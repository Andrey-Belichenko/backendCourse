from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.exceptions.exceptions import WrongDatesOfBookingException, RoomNotFoundException
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM

    mapper = RoomDataMapper

    async def get_valid_rooms_ids(self, hotel_id) -> list:
        query = select(self.model).filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [model.id for model in result.scalars().all()]

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):

        if date_to <= date_from:
            raise WrongDatesOfBookingException

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)

        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rel(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)

        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException

        return RoomDataWithRelsMapper.map_to_domain_entity(model)
