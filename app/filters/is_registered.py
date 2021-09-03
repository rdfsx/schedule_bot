from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.db_api.schemas.user import User


class RegisterFilter(BoundFilter):
    key = 'is_registered'

    async def check(self, message: types.Message):
        user = await User.get(message.from_user.id)
        return False if user.group_id else True
