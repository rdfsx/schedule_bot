from app.loader import scheduler
from app.utils.db import db_gino
from app.utils.apscheduler_jobs import schedule_jobs
from app.utils.set_bot_commands import set_default_commands

from app import middlewares, filters

from app.loader import dp

from app.utils.misc import logger

from aiogram import executor

from app.utils.notify_admins import on_startup_notify


async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)

    await logger.setup()

    print("Подключаем БД")
    # await asyncio.sleep(7)
    await db_gino.on_startup(dp)
    print("Готово")

    await on_startup_notify(dp)
    await set_default_commands(dp)
    schedule_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
