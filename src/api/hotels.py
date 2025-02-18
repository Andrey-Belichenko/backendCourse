from datetime import date

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache

from src.exceptions.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.services.hotels import HotelsService
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await HotelsService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelsService(db).delete_hotel(hotel_id=hotel_id)
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
    hotel = await HotelsService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelsService(db).edit_hotel(hotel_data, hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="", description="")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    """Частичное изменение записи отеля в БД"""
    await HotelsService(db).edit_hotel(hotel_data,
                                       hotel_id,
                                       True)
    return {"status": "OK"}
