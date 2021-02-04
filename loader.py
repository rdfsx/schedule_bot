from aiogram import Bot, Dispatcher, types

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.contrib.fsm_storage.redis import RedisStorage2

import config

from utils.db_api.db_gino import db

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

__all__ = ['bot', 'storage', 'dp', 'db']
