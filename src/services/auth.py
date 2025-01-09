from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from exceptions.exceptions import UnauthorizedUserException, IncorrectTokenException, ObjectAlreadyExistException, \
    UserAlreadyExistException, EmailNotRegisteredException, IncorrectPasswordException
from schemas.users import UserRequestAdd
from services.base import BaseService
from src.config import settings


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_access_token_with_check(self, request):
        access_token = request.cookies.get("access_token", None)
        if not access_token:
            raise UnauthorizedUserException
        return access_token

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hashed_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def get_one_user_with_hashed_password(self, email):
        user = await self.db.users.get_user_with_hashed_password(email=email)

        return user

    async def login_user(self, data: UserRequestAdd) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def logout_user(self, request, response):
        self.get_access_token_with_check(request)
        response.delete_cookie("access_token")

    async def get_current_user(self, request, user_id):
        access_token = self.get_access_token_with_check(request)
        print(f"{access_token=}")
        data = AuthService().decode_token(access_token)
        user_id = data["user_id"]
        user = await self.db.users.get_one_or_none(id=user_id)

        return user

    async def register_user(self, new_user_data):
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistException:  # noqa: E722
            raise UserAlreadyExistException
