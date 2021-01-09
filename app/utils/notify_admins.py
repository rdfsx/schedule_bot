from typing import List, Union
import logging

from app.utils import Broadcast


async def notify_admins(admins: Union[List[int], List[str], int, str]):
    count = await (Broadcast(admins, 'The bot is running!')).start()
    logging.info(f"{count} admins received messages")
