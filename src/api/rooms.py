from fastapi import APIRouter, Body, Query
from datetime import date

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(db: DBDep,
                    hotel_id: int,
                    date_from: date = Query(example="2024-08-01"),
                    date_to: date = Query(example="2024-08-10")):
    """ Получение всех записей номеров из БД """

    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_hotel(db: DBDep,
                        hotel_id: int,
                        room_id: int):
    """ Получение одной записи номера отеля """
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

    return room


@router.post("/{hotel_id}/rooms/{room_id}")
async def create_room(db: DBDep,
                      hotel_id: int,
                      room_data: RoomAddRequest = Body(openapi_examples={
                        "1": {"summary": "Сочи", "value": {
                            "title": "Номер в отеле у моря 5 звезд",
                            "description": "По адресу: Сочи, ул. приморская 7",
                            "price": 0,
                            "quantity": 0}},
                        "2": {"summary": "Dubai", "value": {
                            "title": "Room in hotel 5 stars",
                            "location": "address is Dubai, st. Sea 16"},
                            "price": 0,
                            "quantity": 0}
                            })):
    """ Создание новой записи отеля в БД """

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    hotel = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_hotel(db: DBDep,
                     hotel_id: int,
                     room_id: int,
                     room_data: RoomAddRequest):
    """ Полное изменение записи номера отеля в БД """
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(db: DBDep,
                       hotel_id: int,
                       room_id: int):

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
              summary="",
              description="")
async def patch_hotel(db: DBDep,
                      hotel_id: int,
                      room_id: int,
                      room_data: RoomPatchRequest ):
    """ Частичное изменение записи номера отеля в БД """
    _patch_data = RoomPatch(room_id=room_id, hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(room_data, True, id=room_id)
    await db.commit()

    return {"status": "OK"}
