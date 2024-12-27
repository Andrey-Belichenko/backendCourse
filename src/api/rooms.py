from fastapi import APIRouter, Body, Query
from datetime import date

from exceptions.exceptions import (HotelNotFoundHTTPException, RoomNotFoundHTTPException, RoomNotFoundException,
                                   HotelNotFoundException)
from services.rooms import RoomService
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    """Получение всех записей номеров из БД"""
    rooms = await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)

    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(db: DBDep, hotel_id: int, room_id: int):
    """Получение одной записи номера отеля"""
    try:
        room = await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return room


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    """Создание новой записи номера в БД"""
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep,
                    hotel_id: int,
                    room_id: int,
                    room_data: RoomAddRequest):
    """Полное изменение записи номера отеля в БД"""
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: DBDep,
                     hotel_id: int,
                     room_id: int,
                     room_data: RoomPatchRequest):
    """Частичное изменение записи номера отеля в БД"""
    await RoomService(db).patch_room(hotel_id, room_id, room_data)

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)

    return {"status": "OK"}
