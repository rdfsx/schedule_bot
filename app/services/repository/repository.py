from functools import lru_cache
from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.repository.base_repository import BaseRepository

T = TypeVar("T", bound=BaseRepository)


class Repositories:
    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)
