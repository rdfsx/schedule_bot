from aiogram.dispatcher import Dispatcher
from app.models.base import db

import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from .database import DatabaseMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    env_context = {
        'db': db
    }
    dp.middleware.setup(EnvironmentMiddleware(env_context))
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(DatabaseMiddleware())
    logging.info('Middlewares are successfully configured')
