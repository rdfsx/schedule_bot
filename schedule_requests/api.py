from typing import Optional, Any, Dict

import aiohttp

DEFAULT_DB_URL = "http://rasp.gstu.by/rasp_df/db/"


class API:
    def __init__(self,  url: Optional[str] = None):
        self.db_url = url or DEFAULT_DB_URL

    async def request(self, method: str, params: Dict[str, Any]) -> str:
        url = self.db_url + method + ".php?"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.text()
