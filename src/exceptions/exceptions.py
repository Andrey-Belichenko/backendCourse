from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class WrongDatesOfBookingException(NabronirovalException):
    detail = "Не верные даты бронирования"


class ObjectDoseNotExistException(NabronirovalException):
    detail = "Объект не существует"


class ObjectAlreadyExistException(NabronirovalException):
    detail = "Объект уже существует"


class UnauthorizedUserException(NabronirovalException):
    detail = "Пользователь не авторизован"


class UserAlreadyExistException(NabronirovalException):
    detail = " Пользователь с таким email уже существует "


class IncorrectTokenException(NabronirovalException):
    detail = "Не верный токен"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class UserWithThisEmailAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован "


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль не верный"


class UnauthorizedUserHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пользователь не авторизован"


class UserAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = " Пользователь с таким email уже существует "


class IncorrectTokenHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не верный токен"



