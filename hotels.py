from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(id: int | None = Query(default=None, description="ID"),
               title: str | None = Query(default=None, description="Название отеля"),
               page: int | None = Query(default=1, description="page"),
               per_page: int | None = Query(default=3, description="page"),):
    """ Получение всех записей отелей из БД """
    hotels_ = []
    first_hotel_index_in_page = (page*per_page)-per_page
    last_hotel_index_in_page = page*per_page

    for hotel in hotels[first_hotel_index_in_page:last_hotel_index_in_page]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    """ Удаление записи отеля из БД """
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель у моря 5 звезд",
        "name": "Sochi u moria"}},
    "2": {"summary": "Dubai", "value": {
        "title": "Dubai hotel 5 stars",
        "name": "Dubai hotel"}}
})):
    """ Создание новой записи отеля в БД """
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
        })
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

