from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM

    schema = Room

    async def get_all(self,
                     title,
                     description,
                     price,
                     limit,
                     offset
    ):
        query = select(RoomsORM)

        if price:
            query = query.filter(price)
        if title:
            query = query.filter(func.lower(RoomsORM.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsORM.description).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
