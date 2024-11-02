from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH
from src.repositories.rooms import RoomsRepository
from src.config import settings


router = APIRouter(prefix="/rooms", tags=["Номера отелей"])


@router.get("")
async def get_rooms(pagination: PaginationDep,
                    title: str | None = Query(default=None, description="Название номера"),
                    description: str | None = Query(default=None, description="Описание номера"),
                    price: int | None = Query(default=None, description="Цена номера")
                    ):
    """ Получение всех записей номеров из БД """
    per_page = pagination.per_page or settings.DEFAULT_PAGINATION

    async with (async_session_maker() as session):
        rooms = await RoomsRepository(session).get_all(
            title,
            description,
            price,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

        return rooms


@router.get("/{room_id}")
async def get_one_hotel(room_id: int):
    """ Получение одной записи номера отеля """
    async with (async_session_maker() as session):
        hotel = await RoomsRepository(session).get_one_or_none(id=room_id)

        return hotel


@router.post("")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "hotel_id": 0,
        "title": "Номер в отеле у моря 5 звезд",
        "description": "По адресу: Сочи, ул. приморская 7",
        "price": 0,
        "quantity": 0}},
    "2": {"summary": "Dubai", "value": {
        "hotel_id": 1,
        "title": "Room in hotel 5 stars",
        "location": "address is Dubai, st. Sea 16"},
        "price": 0,
        "quantity": 0}
        })):
    """ Создание новой записи отеля в БД """
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{room_id}")
async def edit_hotel(room_id: int, hotel_data: RoomAdd):
    """ Полное изменение записи номера отеля в БД """
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{rooms_id}")
async def delete_hotel(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}",
              summary="",
              description="")
async def patch_hotel(room_id: int, room_data: RoomPATCH):
    """ Частичное изменение записи номера отеля в БД """
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, True, id=room_id)
        await session.commit()

    return {"status": "OK"}

