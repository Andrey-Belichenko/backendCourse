from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM

    schema = Booking

    async def get_all(self,
                     title,
                     description,
                     price,
                     limit,
                     offset
    ):
        query = select(self.model)

        if price:
            query = query.filter(price)
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(self.model.description).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
