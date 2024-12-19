from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from exceptions.exceptions import WrongDatesOfBookingException, ObjectDoseNotExistException
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep
from src.config import settings

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    """Получение всех записей отелей из БД"""

    per_page = pagination.per_page or settings.DEFAULT_PAGINATION

    #
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )
    try:
        hotels = await db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )
    except WrongDatesOfBookingException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return hotels


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await db.hotels.get_one_or_none(hotel_id=hotel_id)
    except ObjectDoseNotExistException:
        raise HTTPException(status_code=404, detail="Отеля не существует")

    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель у моря 5 звезд",
                    "location": "Сочи, ул. приморская 7",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {"title": "Hotel 5 stars", "location": "Dubai, st. Sea 16"},
            },
        }
    ),
):
    """Создание новой записи отеля в БД"""

    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="", description="")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    """Частичное изменение записи отеля в БД"""

    await db.hotels.edit(hotel_data, True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}
