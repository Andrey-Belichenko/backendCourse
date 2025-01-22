from datetime import date

from src.exceptions.exceptions import (check_date_to_after_date_from, ObjectDoseNotExistException,
                                   RoomNotFoundException)
from src.schemas.facilities import RoomFacilitiesAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch, Room
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomService(BaseService):
    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date):

        check_date_to_after_date_from(date_from, date_to)

        rooms = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms

    async def get_room(self, room_id, hotel_id=None):
        room = await self.db.rooms.get_one_with_rel(id=room_id, hotel_id=hotel_id)
        return room

    async def create_room(self,
                          hotel_id: int,
                          room_data: RoomAddRequest):

        await HotelsService(self.db).get_hotel_with_check(hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]

        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

        return room

    async def edit_room(self,
                        hotel_id: int,
                        room_id: int,
                        room_data: RoomAddRequest):

        await HotelsService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        await self.db.rooms.edit(_room_data, room_id=room_id)

        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )

        await self.db.commit()

    async def patch_room(self,
                         hotel_id: int,
                         room_id: int,
                         room_data: RoomPatchRequest):

        await HotelsService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        room_data_dict = room_data.model_dump(exclude_unset=True)
        _patch_data = RoomPatch(room_id=room_id, hotel_id=hotel_id, **room_data_dict)

        await self.db.rooms.edit(_patch_data, exclude_unset=True, room_id=room_id)

        if "facilities_ids" in room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=room_data_dict["facilities_ids"]
            )

        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(room_id=room_id, hotel_id=hotel_id)

        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            room = await self.db.rooms.get_one(id=room_id)
            return room

        except ObjectDoseNotExistException:
            raise RoomNotFoundException
