from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import RoomFacilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM

    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM

    schema = RoomFacilities

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = (select(self.model.facility_id)
                 .filter_by(room_id=room_id))

        result = await self.session.execute(query)

        current_facilities_ids: list[int] = result.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )

            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            delete_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )

            await self.session.execute(delete_m2m_facilities_stmt)

