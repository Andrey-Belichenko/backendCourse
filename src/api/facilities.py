from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    """ Получение удобств """
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep,
                          add_facility: FacilitiesAdd = Body(openapi_examples=
                                                             {"1": {"summary": "Удобство", "value":
                                                             {"title": "Кондиционер"}}
                                                             })):
    """ Создание удобства """

    facility = await db.facilities.add(add_facility)
    await db.commit()

    return {"facility": facility}



