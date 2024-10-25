from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self,
                   data: BaseModel,
                   title,
                   location) -> None:

        if location or title:

            if location and not title:
                edit_hotel_stmt = (update(self.model)
                                   .where(self.model.location == location.strip())
                                   .values(**data.model_dump()))

            if title and not location:
                edit_hotel_stmt = (update(self.model)
                                   .where(self.model.title == title.strip())
                                   .values(**data.model_dump()))

            if location and title:
                edit_hotel_stmt = (update(self.model)
                                   .where(self.model.title == title.strip() and self.model.location == location.strip())
                                   .values(**data.model_dump()))

            await self.session.execute(edit_hotel_stmt)

    async def delete(self,
                     title,
                     location) -> None:

        if location or title:

            if location and not title:
                edit_hotel_stmt = (delete(self.model)
                                   .where(self.model.location == location.strip())
                                   )
            if title and not location:
                edit_hotel_stmt = (delete(self.model)
                                   .where(self.model.title == title.strip())
                                   )
            if location and title:
                edit_hotel_stmt = (delete(self.model)
                                   .where(self.model.title == title.strip() and self.model.location == location.strip())
                                   )

            await self.session.execute(edit_hotel_stmt)

        # print(edit_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(edit_hotel_stmt)
