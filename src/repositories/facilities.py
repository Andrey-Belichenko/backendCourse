from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facilities, RoomFacilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM

    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM

    schema = RoomFacilities
