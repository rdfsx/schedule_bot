import asyncio
import logging
import typing
from asyncio import sleep

from aiogram import Bot
from aiogram.utils import exceptions


class Broadcast:
    def __init__(
        self,
        users: typing.Union[typing.List[int], typing.List[str], int, str],
        text: str,
        disable_notification: bool = False,
        timeout: int = 0.02,
        logger=__name__,
        bot: Bot = None,
    ):
        self.bot = bot if bot else Bot.get_current()
        if isinstance(users, list):
            self.users = users
        elif isinstance(users, int) or isinstance(users, str):
            self.users = [users]
        self.text = text
        self.disable_notification = disable_notification
        self.count = 0
        self.timeout = timeout

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

    async def send_message(self, user_id: typing.Union[int, str]) -> bool:
        try:
            await self.bot.send_message(
                user_id, self.text, disable_notification=self.disable_notification
            )
        except exceptions.BotBlocked:
            self.logger.debug(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            self.logger.debug(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            self.logger.debug(
                f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
            )
            await sleep(e.timeout)
            return await self.send_message(user_id)  # Recursive call
        except exceptions.UserDeactivated:
            self.logger.debug(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            self.logger.exception(f"Target [ID:{user_id}]: failed")
        else:
            self.logger.debug(f"Target [ID:{user_id}]: success")
            return True
        return False

    async def start(self) -> int:
        for user_id in self.users:
            if await self.send_message(user_id):
                self.count += 1
            await asyncio.sleep(self.timeout)
        return self.count
