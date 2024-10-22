from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(url=settings.DB_URL)   # можно сделать echo=True для отображения SQL запроса

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class BaseORM(DeclarativeBase):
    pass
