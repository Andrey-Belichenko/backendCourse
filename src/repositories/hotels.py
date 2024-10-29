from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
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
