from aiogram import types
from aiogram.dispatcher.filters import Command

from data.convert import sticker

from keyboards.inline import search_kb
from keyboards.inline.inline_buttons import search_teacher

from loader import dp
from states import States


@dp.message_handler(Command('reset'))
async def do_reset(message: types.Message):
    """
    Команда для сброса настроек.
    Дальнейшие запросы опрабатываются в файле start.py
    """
    await States.GROUP.set()
    await message.answer('Найди свою группу:', reply_markup=search_kb)


@dp.message_handler(Command('prepods'))
async def get_prepods_command(message: types.Message):
    """
    Отвечает кнопкой с инлайн меню с преподавателями.
    Обрабатывается в файле inline_handlers.py
    """
    await message.answer('Нажмите на кнопку ниже, чтобы посмотреть рейтинг, либо просто отправьте боту фамилию.',
                         reply_markup=search_teacher)


@dp.message_handler(Command('calls'))
async def get_sticker(message: types.Message):
    """
    Отправляет стикер с расписанием звонков.
    """
    await message.answer_sticker(sticker=sticker)


@dp.message_handler(Command('search'))
async def get_group_schedule(message: types.Message):
    """
    Отвечает кнопкой с возможность
    """
    await message.answer('Нажмите на кнопку ниже и начинайте вводить или просто отправьте боту название группы.',
                         reply_markup=search_teacher)
