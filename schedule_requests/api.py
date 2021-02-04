from typing import Optional, Any, Dict

import aiohttp

DEFAULT_DB_URL = "http://rasp.gstu.by/rasp_df/db/"


class API:
    def __init__(self,  url: Optional[str] = None):
        self.db_url = url or DEFAULT_DB_URL

    async def request(self, method: str, params: Dict[str, Any], timeout: Optional[int] = 3) -> str:
        url = self.db_url + method + ".php?"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.75 Safari/537.36",
            "accept": "*/*"
        }
        print(url)
        print(params)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params, headers=headers, timeout=timeout) as response:
                return await response.text()
