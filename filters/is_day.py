from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.convert import to_eng, to_rus


class DayFilter(BoundFilter):
    key = 'is_day'

    async def check(self, message: types.Message):
        print(message.text.lower() in to_rus)
        return message.text.lower() in to_rus
