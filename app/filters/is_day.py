from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.constants.convert import to_rus


class DayFilter(BoundFilter):
    key = 'is_day'

    async def check(self, message: types.Message):
        return message.text.lower() in to_rus
