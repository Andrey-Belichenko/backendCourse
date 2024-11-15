from fastapi import APIRouter, Body, Query
from datetime import date

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.schemas.facilities import RoomFacilitiesAdd


router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(db: DBDep,
                    hotel_id: int,
                    date_from: date = Query(example="2024-08-01"),
                    date_to: date = Query(example="2024-08-10")):
    """ Получение всех записей номеров из БД """

    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(db: DBDep,
                        hotel_id: int,
                        room_id: int):
    """ Получение одной записи номера отеля """
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

    return room


@router.post("/{hotel_id}/rooms/{room_id}")
async def create_room(db: DBDep,
                      hotel_id: int,
                      room_data: RoomAddRequest = Body()):
    """ Создание новой записи отеля в БД """

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_hotel(db: DBDep,
                     hotel_id: int,
                     room_id: int,
                     room_data: RoomAddRequest):
    """ Полное изменение записи номера отеля в БД """

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(_room_data, id=room_id)

    rooms_facilities_data = [RoomFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]

    existing_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    #existing_facilities = await db.rooms_facilities.get_all()

    await db.rooms_facilities.edit_bulk(rooms_facilities_data, existing_data=existing_facilities)

    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(db: DBDep,
                      hotel_id: int,
                      room_id: int,
                      room_data: RoomPatchRequest):
    """ Частичное изменение записи номера отеля в БД """
    _patch_data = RoomPatch(room_id=room_id, hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(room_data, True, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(db: DBDep,
                       hotel_id: int,
                       room_id: int):

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}


