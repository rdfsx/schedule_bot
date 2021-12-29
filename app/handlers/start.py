from typing import Callable

from aiogram import Dispatcher
from aiogram.types import Message
from sqlalchemy.orm import Session, sessionmaker

from app.constants.convert import start_sticker
from app.services.repository.repository import Repositories
from app.services.repository.user_repository import UserRepository
from app.states import StartStates


async def begin_registration(m: Message):
    await StartStates.GROUP.set()
    await m.answer_sticker(sticker=start_sticker)
    await m.answer(f"Приветствую, {m.from_user.full_name}!\n"
                   "Найди свою группу:", reply_markup=search_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(begin_registration, commands="start")
