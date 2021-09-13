from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.db_api.commands.coomands_group import select_group


class GroupFilter(BoundFilter):
    key = 'is_group'

    async def check(self, message: types.Message) -> bool:
        return await select_group(message.text, True)
