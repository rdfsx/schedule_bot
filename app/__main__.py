from app.loader import db, scheduler
from app.utils.db_api import db_gino
from app.utils.misc.apscheduler_jobs import schedule_jobs
from app.utils.set_bot_commands import set_default_commands

from app import middlewares, filters, handlers

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

    print("Создаем таблицы")
    await db.gino.create_all()

    await on_startup_notify(dp)
    await set_default_commands(dp)
    schedule_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
