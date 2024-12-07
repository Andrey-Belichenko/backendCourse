from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.schemas.bookings import Booking
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User
from src.schemas.facilities import Facilities
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facilities
