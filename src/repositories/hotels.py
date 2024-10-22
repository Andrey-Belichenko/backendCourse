from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


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

    async def add(self, hotel_data: Hotel):
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await self.session.execute(add_hotel_stmt)
        return add_hotel_stmt.compile().params
