from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor

from app.models import base
from app import utils, config
from app import handlers, middlewares


async def on_startup(dispatcher: Dispatcher):
    handlers.setup(dp)
    middlewares.setup(dp)
    await base.connect(config.POSTGRES_URI)
    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins(config.SUPERUSER_IDS)


async def on_shutdown(dispatcher: Dispatcher):
    await base.close_connection()


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = RedisStorage2(config.REDIS_HOST, config.REDIS_PORT)
    dp = Dispatcher(bot=bot, storage=storage)
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=config.SKIP_UPDATES
    )
