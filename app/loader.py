from aiogram import Bot, Dispatcher, types

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from app import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST)
# storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']
