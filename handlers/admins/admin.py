from asyncio import create_task

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, TelegramAPIError

from config import admins
from data.messages import hello_message
from keyboards.default import menu
from keyboards.inline.callback_datas import message_for_admin
from keyboards.inline.inline_buttons import cancel_markup
from loader import dp, bot

from states.admin_state import AnswerAdmin, BroadcastAdmin

from utils.admin_tools.broadcast import broadcaster
from utils.db_api.commands.commands_user import select_all_users, count_users


@dp.message_handler(Command('count'), user_id=admins)
async def get_count_users(message: types.Message):
    count = await count_users()
    await message.answer(f"Количество пользователей в базе: {count}")


@dp.message_handler(Command('broadcast'), user_id=admins)
async def broadcast_message(message: types.Message):
    await BroadcastAdmin.BROADCAST.set()
    await message.answer('Введите сообщение, которое хотели бы отправить всем, кто есть в базе:',
                         reply_markup=cancel_markup)


@dp.callback_query_handler(text='cancel', state='*', user_id=admins)
async def cancel_broadcast(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.answer()
    await call.message.answer('Отменено.')


@dp.message_handler(state=BroadcastAdmin.BROADCAST, user_id=admins)
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


@dp.callback_query_handler(message_for_admin.filter(), user_id=admins)
async def get_other_schedule(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await AnswerAdmin.ANSWER.set()
    await state.update_data({
        'message_id': callback_data.get('message_id'),
        'from_user_id': callback_data.get('from_user_id')
    })
    await call.answer()
    await call.message.answer("Введите сообщение:", reply_markup=cancel_markup)


@dp.message_handler(state=AnswerAdmin.ANSWER, user_id=admins)
async def answer_to_user_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.send_message(chat_id=data.get('from_user_id'),
                               reply_to_message_id=data.get('message_id'),
                               text=message.text)

    except BotBlocked:
        await message.reply("Сообщение не отправлено: бот заблокирован пользователем.")
    except UserDeactivated:
        await message.reply("Сообщение не отправлено: пользователь удалил свой аккаунт.")
    except TelegramAPIError:
        await message.reply("Сообщение не отправлено: ошибка на стороне телеграма.")
    else:
        await message.reply("Сообщение отправлено!")

    await state.reset_state()


@dp.message_handler(Command('add_group'), user_id=admins)
async def add_group(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(Command('add_teacher'), user_id=admins)
async def add_group(message: types.Message, state: FSMContext):
    pass
