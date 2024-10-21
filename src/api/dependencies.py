from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="page", gt=0)]
    per_page: Annotated[int | None, Query(default=3, description="per_page", gt=0, lt=30)]


PaginationDep = Annotated[PaginationParams,  Depends()]
