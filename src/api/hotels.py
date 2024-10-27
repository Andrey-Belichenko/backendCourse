from fastapi import Query, Body, APIRouter

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(default=None, description="Название отеля"),
                     location: str | None = Query(default=None, description="Адрес отеля")
                     ):
    """ Получение всех записей отелей из БД """
    per_page = pagination.per_page or 5

    async with (async_session_maker() as session):
        hotels = await HotelsRepository(session).get_all(
            location,
            title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

        return hotels


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int):
    async with (async_session_maker() as session):
        hotel = await HotelsRepository(session).get_one_or_none_hotel(hotel_id)

        return hotel


@router.delete("")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель у моря 5 звезд",
        "location": "Сочи, ул. приморская 7"}},
    "2": {"summary": "Dubai", "value": {
        "title": "Hotel 5 stars",
        "location": "Dubai, st. Sea 16"}}
        })):
    """ Создание новой записи отеля в БД """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="",
              description="")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    """ Частичное изменение записи отеля в БД """
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}
