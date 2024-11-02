from pydantic import BaseModel, ConfigDict


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    title: str | None = None
    hotel_id: int | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

