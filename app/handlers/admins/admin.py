import asyncio

from asyncpg import UniqueViolationError
from loguru import logger
from asyncio import create_task

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, TelegramAPIError

from app.config import admins
from app.keyboards.inline.callback_datas import message_for_admin
from app.keyboards.inline.inline_buttons import cancel_markup
from app.loader import dp, bot
from app.schedule_requests.api_group import APIMethodsGroup
from app.states.admin_state import AnswerAdmin, BroadcastAdmin
from app.utils.admin_tools.broadcast import broadcaster
from app.utils.db_api.commands.commands_user import select_all_users, count_users, count_users_with_group, add_user
from app.utils.db_api.schemas import User


@dp.message_handler(Command('count'), user_id=admins)
async def get_count_users(message: types.Message):
    count = await count_users()
    await message.answer(f"Количество пользователей в базе: {count}")


@dp.message_handler(Command('group_count'), user_id=admins)
async def get_count_users_with_group(message: types.Message):
    count = await count_users_with_group()
    await message.answer(f"Количество пользователей, выбравших группу: {count}")


@dp.message_handler(Command("get_users"), user_id=admins)
async def get_users(message: types.Message):
    await message.answer("start")
    file = open('users.txt', "r")
    for line in file:
        await add_user(user_id=int(line.replace("\n", "")))
    file.close()
    await message.answer("finish")


@dp.message_handler(Command('exists_count'), user_id=admins)
async def get_exists_count(message: types.Message):
    users = await select_all_users()
    count = 0
    await message.answer("Начинаем подсчет...")
    try:
        for user in users:
            try:
                if await bot.send_chat_action(user.id, "typing"):
                    count += 1
            except Exception as e:
                logger.exception(e)
            await asyncio.sleep(.05)
    finally:
        for admin in admins:
            await bot.send_message(admin, f"{count} активных пользователей.")


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


@dp.message_handler(state=AnswerAdmin.ANSWER, user_id=admins, content_types=types.ContentType.ANY)
async def answer_to_user_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await message.send_copy(data.get('from_user_id'), reply_to_message_id=data.get('message_id'))

    except BotBlocked:
        await message.reply("Сообщение не отправлено: бот заблокирован пользователем.")
    except UserDeactivated:
        await message.reply("Сообщение не отправлено: пользователь удалил свой аккаунт.")
    except TelegramAPIError:
        await message.reply("Сообщение не отправлено: ошибка на стороне телеграма.")
    else:
        await message.reply("Сообщение отправлено!")

    await state.reset_state()


@dp.message_handler(Command('update_schedule'), user_id=admins, state='*')
async def update_schedule(message: types.Message):
    await message.answer("Начинаем обновлять расписание...")
    create_task(APIMethodsGroup().compare_all_groups())


@dp.message_handler(Command('backup'), user_id=admins)
async def do_packup(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(Command('add_group'), user_id=admins)
async def add_group(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(Command('add_teacher'), user_id=admins)
async def add_teacher(message: types.Message, state: FSMContext):
    pass
