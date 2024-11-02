from fastapi import APIRouter, HTTPException, Response, Request

from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        ):
    hashed_password = AuthService().hashed_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:

        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        ):
    # hashed_password = pwd_context.hash(data.password)
    # new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:

        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован ")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.get("/me")
async def me(
        request: Request,
        user_id: UserIdDep,
        ):

    access_token = request.cookies.get('access_token', None)
    data = AuthService().encode_token(access_token)

    user_id = data["user_id"]

    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)

    return user


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        ):

    access_token = request.cookies.get('access_token', None)

    if not access_token:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")

    response.delete_cookie("access_token")

    return {"status ": "200"}
