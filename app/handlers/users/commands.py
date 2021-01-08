from aiogram import types
from aiogram.dispatcher.filters import Command

from app.data import sticker

from app.keyboards.inline import search_kb
from app.keyboards.inline import search_teacher

from app.loader import dp
from app.states import States


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
