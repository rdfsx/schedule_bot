import typing
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.services.repository.base import BaseRepository, Model
from app.utils.db.utils import filter_payload, manual_cast


class UserRepository(BaseRepository[User]):
    model = User

    async def add_user(self, *, user_id: int, group: Optional[str] = None, subgroup: Optional[int] = 1) -> Model:
        prepared_payload = filter_payload(locals())
        return manual_cast(await self._insert(**prepared_payload))

    async def delete_user(self, user_id: int) -> None:
        try:
            await self._delete(self.model.id == user_id)
        except IntegrityError:
            raise UnableToDelete()

    async def get_user_by_username(self, username: str) -> Model:
        return manual_cast(await self._select_one(self.model.username == username))

    async def get_user_by_id(self, user_id: int) -> Model:
        return manual_cast(await self._select_one(self.model.id == user_id))

    async def get_all_users(self) -> typing.List[Model]:
        return manual_cast(await self._select_all(), typing.List[Model])

    async def get_users_count(self) -> int:
        return await self._count()
