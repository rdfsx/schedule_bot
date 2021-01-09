from aiogram import Dispatcher
from aiogram import filters

from .start import command_start_handler


def setup(dp: Dispatcher):
    dp.register_message_handler(command_start_handler, filters.Command('start', ignore_mention=True))
