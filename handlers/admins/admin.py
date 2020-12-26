from asyncio import create_task

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.dispatcher.filters import Command

from config import admins
from loader import dp

from states.admin_state import StatesAdmin

from utils.admin_tools.broadcast import broadcaster
from utils.db_api.commands.commands_user import select_all_users, count_users


@dp.message_handler(Command('count'), user_id=admins)
async def get_count_users(message: types.Message):
    count = await count_users()
    await message.answer(f"Количество пользователей в базе: {count}")


@dp.message_handler(Command('broadcast'), user_id=admins)
async def broadcast_message(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ])
    await StatesAdmin.BROADCAST.set()
    await message.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:', reply_markup=markup)


@dp.callback_query_handler(text='cancel', state=StatesAdmin.BROADCAST, user_id=admins)
async def cancel_broadcast(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.answer()
    await call.message.answer('Отменено.')


@dp.message_handler(state=StatesAdmin.BROADCAST, user_id=admins)
async def broadcast_to_users(message: types.Message, state: FSMContext):
    users = await select_all_users()
    create_task(broadcaster(users, message.text))
    await state.reset_state()
    txt = [
        'Сообщение рассылается пользователям.',
        'Как только все пользователи его получат,',
        'админам придёт уведомление.'
    ]
    await message.answer('\n'.join(txt))
