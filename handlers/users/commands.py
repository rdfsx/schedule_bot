from aiogram import types
from aiogram.dispatcher.filters import Command

from data.convert import sticker
from data.messages import hello_message
from keyboards.default import menu
from keyboards.inline import search_kb
from keyboards.inline.inline_buttons import search_teacher
from loader import dp
from states import States


@dp.message_handler(Command('reset'))
async def do_reset(message: types.Message):
    await States.GROUP.set()
    await message.answer('Найди свою группу:', reply_markup=search_kb)


@dp.message_handler(Command('prepods'))
async def get_prepods_command(message: types.Message):
    await message.answer('Нажмите на кнопку ниже, чтобы посмотреть рейтинг, либо просто отправьте боту фамилию.',
                         reply_markup=search_teacher)


@dp.message_handler(Command('calls'))
async def get_sticker(message: types.Message):
    await message.answer_sticker(sticker=sticker)


@dp.message_handler(Command('search'))
async def get_group_schedule(message: types.Message):
    await message.answer('Нажмите на кнопку ниже и начинайте вводить или просто отправьте боту название группы.',
                         reply_markup=search_teacher)


@dp.message_handler(Command('b'))
async def get_kb(message: types.Message):
    await message.answer(hello_message, reply_markup=menu, disable_web_page_preview=True)


@dp.message_handler(Command('info'))
async def get_kb(message: types.Message):
    text = [
        "Ботдаёт возможнность просматривать расписание групп и преподавателей ГГТУ Сухого.",
        "Доступны команды:",
        "/prepods - рейтинг и расписание преподавателей",
        "/calls - стикер с расписанием звонков",
        "/search - расписание чужой группы",
        "/start или /reset - сброс настроек"
    ]
    await message.answer("\n\n".join(text), reply_markup=menu)
