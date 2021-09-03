import asyncio

from aiogram.utils import exceptions
from loguru import logger

from app.config import admins
from app.loader import bot


async def send_message(user_id: int, txt: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param txt:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, txt, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, txt)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(users, msg: str, disable_notification: bool = False) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for user in users:
            if await send_message(user.id, msg, disable_notification):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info(f"{count} messages successful sent.")
        for admin in admins:
            await bot.send_message(admin, f"{count} сообщений отправлено.")
    return count
