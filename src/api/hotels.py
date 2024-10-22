from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select

from src.models.hotels import HotelsORM
from src.database import async_session_maker, engine
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
        query = select(HotelsORM)
        if location:
            query = query.filter(query.c.location.contains(location))
        if title:
            query = query.filter(query.c.title.contains(title))
        query = (
                query
                .limit(per_page)
                .offset(per_page * (pagination.page-1))
                )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    """ Удаление записи отеля из БД """
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
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
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    """ Полное изменение записи БД """
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}
    return {"status:": "ID ERROR"}


@router.patch("/{hotel_id}",
              summary="",
              description="")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    """ Частичное изменение записи отеля в БД """
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name

            return {"status": "OK"}
    return {"status:": "ID ERROR"}

