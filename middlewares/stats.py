import asyncio
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import config
from utils.stats import send_statistics


class StatisticMiddleware(BaseMiddleware):
    """
    Мидлварь для отправки статистики на chatbase.com
    """

    def __init__(self):
        super(StatisticMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: types.Message, data: dict):
        loop = asyncio.get_event_loop()
        send_statistics(loop, config.STATISTICS_TOKEN, message.chat.id, message.text)
