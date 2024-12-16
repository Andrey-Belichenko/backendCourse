from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM

    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
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

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)

        result = await self.session.execute(query)

        model = result.scalars().unique().one_or_none()

        if not model:
            return None

        return RoomDataWithRelsMapper.map_to_domain_entity(model)
