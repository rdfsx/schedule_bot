from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.repository.repository import Repositories


class RepoMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['update']

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session: AsyncSession = data['session']
        data["repo"] = Repositories(session)
