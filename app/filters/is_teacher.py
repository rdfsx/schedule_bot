from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.db_api.commands.commands_teacher import select_teacher_by_name


class TeacherFilter(BoundFilter):
    key = 'is_teacher'

    async def check(self, message: types.Message) -> bool:
        if 1 < len(message.text) < 50 and message.text.replace(" ", "").replace(".", "").isalpha():
            return await select_teacher_by_name(message.text)
