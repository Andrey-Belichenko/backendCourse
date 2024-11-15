from sqlalchemy import select, insert, update, delete, func

from pydantic import BaseModel


class BaseRepository:
    model = None

    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self,
                           *filter,
                           **filter_by,
                           ):

        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)

        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if not model:
            return None

        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (insert(self.model)
                         .values(**data.model_dump())
                         .returning(self.model))

        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = (insert(self.model)
                         .values([item.model_dump() for item in data]))

        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        update_stmt = (update(self.model)
                       .filter_by(**filter_by)
                       .values(**data.model_dump(exclude_unset=exclude_unset)))

        await self.session.execute(update_stmt)

    async def edit_bulk(self, data: list[BaseModel],
                        existing_data: list[BaseModel],
                        exclude_unset=False, **filter_by) -> None:

        request_facilities_list = [item for item in data]
        existing_facilities_list = [item for item in existing_data]

        # update_stmt = (update(self.model)
        #                .filter_by(**filter_by)
        #                .values([item.model_dump(exclude_unset=exclude_unset) for item in data]))

        # await self.session.execute(update_stmt)

        list_for_delete = [x for x in existing_facilities_list if x not in request_facilities_list]

        list_for_add = [x for x in request_facilities_list if x not in existing_facilities_list]

        await self.add_bulk(list_for_add)
        await self.delete_bulk(list_for_delete)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def delete_bulk(self, record_obj) -> None:
        obj_ids = [obj.id for obj in record_obj]
        query = await self.session.select(self.model).filter(self.model.id.in_(obj_ids))
        await query.delete(synchronize_session=False)
        # delete_stmt = delete(self.model).filter_by(**filter_by)
        # await self.session.execute(delete_stmt)
