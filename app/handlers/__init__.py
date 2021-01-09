import logging

from aiogram import Dispatcher

from . import private, errors


def setup(dp: Dispatcher):
    errors.setup(dp)
    private.setup(dp)
    logging.info("Handlers are successfully configured")
