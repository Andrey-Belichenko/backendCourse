class UnableRoomBookingException(Exception):
    def __init__(self, status_code, room_id):
        self.room_id = room_id
        self.status_code = status_code

    def __str__(self):
        return (f"Status code: {self.status_code}, "
                f"Message: Невозможно создать бронирование номера {self.room_id}")

    def __repr__(self):
        class_name = self.__class__.__name__
        return (f"{class_name} Status code: {self.status_code!r}, "
                f"Message: Невозможно создать бронирование номера {self.room_id!r}")
