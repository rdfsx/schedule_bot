from loguru import logger

import asyncio
import aiohttp

from app.config import STATISTICS_TOKEN

from chatbase import Message


class AsyncMessage(Message):
    def __init__(self, user_id, message, intent: str = "", not_handled: bool = False):
        self.api_key = STATISTICS_TOKEN
        self.platform = "tg"
        Message.__init__(self,
                         api_key=self.api_key,
                         platform=self.platform,
                         user_id=user_id,
                         message=message,
                         intent=intent,
                         not_handled=not_handled)

    async def _make_request(self):
        url = "https://chatbase.com/api/message"
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                    data=self.to_json(),
                                    headers=Message.get_content_type()) as response:
                logger.info(f"Chatbase response {response}")
                return response

    async def send(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self._make_request())
