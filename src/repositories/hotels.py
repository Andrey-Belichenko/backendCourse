from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM

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
        return result.scalars().all()

    async def get_one_or_none_hotel(self, hotel_id):
        query = select(self.model).filter_by(id=hotel_id)

        result = await self.session.execute(query)
        return result.scalars().one_or_none()
