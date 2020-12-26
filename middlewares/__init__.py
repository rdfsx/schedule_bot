from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .stats import StatisticMiddleware
from .acl import ACLMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(StatisticMiddleware())
    dp.middleware.setup(ACLMiddleware())
