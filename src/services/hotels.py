from datetime import date

#from src.config import settings
from src.exceptions.exceptions import check_date_to_after_date_from, ObjectDoseNotExistException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        """Получение всех записей отелей из БД"""

        #per_page = pagination.per_page or settings.DEFAULT_PAGINATION
        per_page = pagination.per_page or 5
        check_date_to_after_date_from(date_from, date_to)

        hotels = await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

        return hotels

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def edit_hotel(self,
                         hotel_data: HotelAdd | HotelPATCH,
                         hotel_id: int, 
                         exclude_unset: bool = False):
        await self.db.hotels.edit(hotel_data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            hotel = await self.db.hotels.get_one(id=hotel_id)
            return hotel

        except ObjectDoseNotExistException:
            raise HotelNotFoundException
