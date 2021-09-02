import logging

from aiogram import Dispatcher
from aiogram.utils.markdown import quote_html

from config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")

        except Exception as err:
            logging.exception(err)


async def notify_new_user(dp: Dispatcher, user_id: int, group: str) -> None:
    user = await dp.bot.get_chat(chat_id=user_id)
    pics = await dp.bot.get_user_profile_photos(user_id)
    txt = [
        "#new_user",
        f"Имя: {quote_html(user.full_name)}",
        f'id: <a href="tg://user?id={user.id}">{user_id}</a>',
        f"Группа: {group}",
        f"username: @{user.username}"
    ]
    for admin in admins:
        try:
            await dp.bot.send_photo(admin, photo=pics.photos[0][-1].file_id, caption=('\n'.join(txt)))

        except IndexError:
            await dp.bot.send_message(admin, '\n'.join(txt))
