from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from exceptions.exceptions import WrongDatesOfBookingException, ObjectDoseNotExistException
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

    async def get_one_or_none_with_rel(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)

        result = await self.session.execute(query)

        model = result.scalars().unique().one_or_none()

        if not model:
            return None

        return RoomDataWithRelsMapper.map_to_domain_entity(model)

    async def edit_room(self, data: BaseModel, room_id, exclude_unset=False) -> None:
        valid_rooms_ids = await self.get_valid_rooms_ids(data.hotel_id)

        if room_id not in valid_rooms_ids:
            raise ObjectDoseNotExistException

        update_stmt = (
            update(self.model)
            .filter_by(id=room_id)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(update_stmt)

    async def delete_room(self, room_id, hotel_id) -> None:

        valid_rooms_ids = await self.get_valid_rooms_ids(hotel_id)

        if room_id not in valid_rooms_ids:
            raise ObjectDoseNotExistException

        delete_stmt = delete(self.model).filter_by(room_id=room_id, hotel_id=hotel_id)
        await self.session.execute(delete_stmt)
