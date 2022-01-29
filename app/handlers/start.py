from aiogram import types, Dispatcher

from app.constants.convert import start_sticker
from app.keyboards.inline import GroupSearchKb
from app.states import StartStates


async def begin_registration(msg: types.Message):
    await StartStates.GROUP.set()
    await msg.answer_sticker(sticker=start_sticker)
    await msg.answer(f"Приветствую, {msg.from_user.full_name}!\n"
                     "Найди свою группу:", reply_markup=GroupSearchKb().get())


def setup(dp: Dispatcher):
    dp.message.register(begin_registration, commands="start")
