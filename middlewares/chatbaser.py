import asyncio

import aiohttp
from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from config import STATISTICS_TOKEN

from chatbase import Message


class AsyncMessage(Message):
    def __init__(self, user_id, message, intent: str = "", not_handled: bool = False):
        self.api_key = STATISTICS_TOKEN
        self.platform = "tg"
        Message.__init__(self,
                         api_key=self.api_key,
                         platform=self.platform,
                         user_id=user_id,
                         message=message,
                         intent=intent,
                         not_handled=not_handled)

    async def _make_request(self):
        url = "https://chatbase.com/api/message"
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                    data=self.to_json(),
                                    headers=Message.get_content_type()) as response:
                return response

    async def send(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self._make_request())


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
