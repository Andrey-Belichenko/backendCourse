import typing

from src.database import BaseORM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

if typing.TYPE_CHECKING:
    from src.models import RoomsORM


class FacilitiesORM(BaseORM):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )


class RoomsFacilitiesORM(BaseORM):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
