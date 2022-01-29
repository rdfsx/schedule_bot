from aiogram import types
from aiogram.dispatcher.filters import Command

from app.constants.convert import sticker
from app.constants.messages import hello_message, donuts
from app.keyboards.default import menu
from app.keyboards.inline_ import search_kb
from app.keyboards.inline_.inline_buttons import search_teacher
from app.loader import dp
from app.states import StartStates


@dp.message_handler(Command('reset'))
async def do_reset(message: types.Message):
    await StartStates.GROUP.set()
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
                         reply_markup=search_kb)


@dp.message_handler(Command('b'))
async def get_kb(message: types.Message):
    await message.answer(hello_message, reply_markup=menu, disable_web_page_preview=True)


@dp.message_handler(Command('info'))
async def get_info(message: types.Message):
    text = [
        "Ботдаёт возможнность просматривать расписание групп и преподавателей ГГТУ Сухого.",
        "Доступны команды:",
        "/prepods - рейтинг и расписание преподавателей",
        "/calls - стикер с расписанием звонков",
        "/search - расписание чужой группы",
        "/start или /reset - сброс настроек"
    ]
    await message.answer("\n\n".join(text), reply_markup=menu)


@dp.message_handler(Command('donuts'))
async def get_donuts(message: types.Message):
    await message.answer(donuts, reply_markup=menu)
