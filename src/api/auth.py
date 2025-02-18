from fastapi import APIRouter, Response, Request

from src.exceptions.exceptions import UserWithThisEmailAlreadyExistHTTPException, \
    IncorrectPasswordHTTPException, UnauthorizedUserException, UnauthorizedUserHTTPException, IncorrectTokenException, \
    IncorrectTokenHTTPException, UserAlreadyExistException, UserAlreadyExistHTTPException, EmailNotRegisteredException,\
    EmailNotRegisteredHTTPException, IncorrectPasswordException
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd, UserAdd
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    hashed_password = AuthService().hashed_password(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    try:
        await AuthService(db).register_user(new_user_data)
    except UserAlreadyExistException:
        raise UserAlreadyExistHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    return {"access_token": access_token}


@router.get("/me")
async def me(
    db: DBDep,
    request: Request,
    user_id: UserIdDep,
):
    try:
        user = await AuthService(db).get_current_user(request, user_id)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return user


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
):
    try:
        await AuthService().logout_user(request, response)
    except UnauthorizedUserException:
        raise UnauthorizedUserHTTPException

    return {"status ": "200"}
