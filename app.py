import asyncio

from app.utils.db_api import db_gino
from app.utils import main
from app.utils import set_default_commands

from app.loader import db


async def on_startup(dp):
    from app import filters
    from app import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from app.utils import on_startup_notify

    from app.utils.misc import logger
    await logger.setup()

    print("Подключаем БД")
    await asyncio.sleep(5)
    await db_gino.on_startup(dp)
    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()

    print("Чистим базу")
    await db.gino.drop_all()

    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()

    await main()

    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from app.handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
