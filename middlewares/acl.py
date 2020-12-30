from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ReplyKeyboardRemove

from loader import bot
from utils.db_api.schemas.user import User


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User):
        user_id = user.id
        user = await User.get(user_id)
        if not user:
            return await bot.send_message(user_id, "Вы не зарегистрированы! Чтобы воспользоваться расписанием, "
                                                   "введите команду /start и проследуйте инструкциям.",
                                          reply_markup=ReplyKeyboardRemove())
        data['user'] = user
        # TODO добавление пользователя в базу

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
