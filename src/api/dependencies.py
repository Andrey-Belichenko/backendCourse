from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.services.auth import AuthService
from src.database import async_session_maker
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="page", gt=0)]
    per_page: Annotated[int | None, Query(None, description="per_page", gt=0, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)

    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")

    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)

    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
