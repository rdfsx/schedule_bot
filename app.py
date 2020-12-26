from loader import db
from utils.db_api import db_gino
from utils.set_bot_commands import set_default_commands
from loguru import logger


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    from utils.misc import logger
    await logger.setup()

    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
