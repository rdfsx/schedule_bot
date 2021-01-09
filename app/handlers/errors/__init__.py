from aiogram import Dispatcher
from aiogram.utils import exceptions

from .retry_after import retry_after_error


def setup(dp: Dispatcher):
    dp.register_errors_handler(retry_after_error, exception=exceptions.RetryAfter)
