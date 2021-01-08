from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .acl import ACLMiddleware
from .chatbaser import ChatbaseMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware())
    dp.middleware.setup(ChatbaseMiddleware())
