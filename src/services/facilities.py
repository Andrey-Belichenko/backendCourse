from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def create_facility(
            self,
            data: FacilitiesAdd
    ):
        """Создание удобства"""

        facility = await self.db.facilities.add(data)
        await self.db.commit()

        return facility

    async def get_facilities(self):
        return await self.db.facilities.get_all()
