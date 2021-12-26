from aiogram import types, Dispatcher
from aiogram.types import BotCommandScopeChat

from app.config import Config


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('b', 'Если исчезли кнопки'),
            types.BotCommand('reset', 'Сброс настроек'),
            types.BotCommand('prepods', 'Рейтинг и расписание преподавателей'),
            types.BotCommand('search', 'Расписание чужой группы'),
            types.BotCommand('donuts', 'Поддержать разработчика'),
            types.BotCommand('calls', 'Стикер с расписанием звонков'),
        ]
    )
    for admin in Config.ADMINS:
        await dp.bot.set_my_commands(
            [
                types.BotCommand("amount", "Количество юзеров в бд"),
                types.BotCommand("chat_amount", "Количество групп в бд"),
                types.BotCommand("chat_users_amount", "Количество пользователей во всех группах"),
                types.BotCommand("exists_amount", "Количество живых юзеров"),
                types.BotCommand("broadcast", "Рассылка по всем юзерам"),
                types.BotCommand("users_file", 'Записать юзеров в файл')
            ],
            BotCommandScopeChat(admin)
        )
