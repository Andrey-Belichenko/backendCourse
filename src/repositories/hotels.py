from datetime import date

from sqlalchemy import select, insert, func

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM

    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsORM)

        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date,
                                   location=None,
                                   title=None,
                                   limit=None,
                                   offset=None,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        query = await self.get_filtered(filter=HotelsORM.id.in_(hotels_ids_to_get),
                                        location=location,
                                        title=title,
                                        limit=limit,
                                        offset=offset,
                                        )

        return query
