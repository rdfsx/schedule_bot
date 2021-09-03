from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.utils.stats import AsyncMessage


class ChatbaseMiddleware(BaseMiddleware):

    @staticmethod
    async def on_pre_process_message(message: types.Message, data: dict, *args, **kwargs):
        data["handled"] = False

    @staticmethod
    async def on_pre_process_callback_query(query: types.CallbackQuery, data: dict, *args, **kwargs):
        data["handled"] = False

    @staticmethod
    async def on_post_process_message(message: types.Message, *args, **kwargs):
        data = args[1]
        if not data.get('handled'):
            msg = AsyncMessage(
                user_id=str(message.from_user.id),
                message=message.text,
                not_handled=True
            )
            await msg.send()

    @staticmethod
    async def on_post_process_callback_query(query: types.CallbackQuery, *args, **kwargs):
        data = args[1]
        if not data.get('handled'):
            msg = AsyncMessage(
                user_id=query.from_user.id,
                message=query.data,
                not_handled=True
            )
            await msg.send()

    @staticmethod
    async def on_process_message(message: types.Message, data: dict):
        handler = current_handler.get()
        if handler:
            handler_name = handler.__name__
            msg = AsyncMessage(
                user_id=str(message.from_user.id),
                message=message.text,
                intent=handler_name
            )
            await msg.send()

    @staticmethod
    async def on_process_callback_query(query: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        if handler:
            handler_name = handler.__name__
            msg = AsyncMessage(
                user_id=query.from_user.id,
                message=query.data,
                intent=handler_name
            )
            await msg.send()
