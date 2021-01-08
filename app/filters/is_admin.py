from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app import config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    async def check(self, message: types.Message):
        return message.from_user.id in config.admins
