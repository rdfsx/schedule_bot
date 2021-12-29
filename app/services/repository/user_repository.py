from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.models.group import GroupModel
from app.models.user import UserModel
from app.services.repository.base_repository import BaseRepository, Model
from app.utils.db.utils import filter_payload, manual_cast
from app.utils.exceptions import UnableToDelete


class UserRepository(BaseRepository[UserModel]):
    model = UserModel

    async def add_user(self, *,
                       user_id: int,
                       group: GroupModel | None = None) -> Model:
        prepared_payload = filter_payload(locals())
        return manual_cast(await self._insert(**prepared_payload))

    async def delete_user(self, user_id: int) -> None:
        try:
            await self._delete(self.model.id == user_id)
        except IntegrityError:
            raise UnableToDelete()

    async def get_user_by_id(self, user_id: int) -> Model:
        return manual_cast(await self._select_one(self.model.id == user_id))

    async def get_all_users(self) -> list[Model]:
        return manual_cast(await self._select_all(), list[Model])

    async def get_users_count(self) -> int:
        return await self._count()
