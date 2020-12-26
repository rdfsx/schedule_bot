from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('b', 'Если исчезли кнопки'),
        types.BotCommand('reset', 'Сброс настроек'),
        types.BotCommand('prepods', 'Рейтинг преподавателей'),
        types.BotCommand('search', 'Расписание чужой группы'),
        types.BotCommand('calls', 'Стикер с расписанием звонков')
    ])
