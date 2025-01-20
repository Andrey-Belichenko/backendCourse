from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.facilities import FacilitiesService
from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    """Получение удобств"""
    return await FacilitiesService(db).get_facilities()


@router.post("")
async def create_facility(
    db: DBDep,
    add_facility: FacilitiesAdd = Body(
        openapi_examples={"1": {"summary": "Удобство", "value": {"title": "Кондиционер"}}}
    ),
):
    """Создание удобства"""

    facility = await FacilitiesService(db).create_facility(add_facility)

    return {"facility": facility}
