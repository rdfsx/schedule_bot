from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.config as config
from app.utils.db.db_gino import db

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage(host=config.REDIS_HOST)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

__all__ = ['bot', 'storage', 'dp', 'db', 'scheduler']
