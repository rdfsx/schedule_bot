from aiogram import types
from gino import Gino

from app.models import User


async def command_start_handler(msg: types.Message, db: Gino):
    print(await db.func.count(User.id).gino.scalar())
    await msg.answer('Hello')
