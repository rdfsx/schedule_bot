from typing import Optional, Any, Dict

import requests
from datetime import datetime

from requests import Response

from models.schedule import FuckultSchedule, Sem

DEFAULT_DB_URL = "http://rasp.gstu.by/rasp_df/db/"


class API:
    def __init__(self,  url: Optional[str] = None):
        self.db_url = url or DEFAULT_DB_URL

    def request(self, method: str, params: Dict[str, Any]) -> Response:
        url = self.db_url + method + ".php?"
        return requests.get(url, params=params, timeout=2)


def request(prepod: str, sem: Sem, fuckult: FuckultSchedule) -> requests.models.Response:
    url = "http://rasp.gstu.by/rasp_df/db/get/getRaspByPrepod.php?"
    date = datetime.now().strftime('%Y-%m-%d')
    params = {
        'prepod': f"'{prepod}'",
        'sem': sem.value,
        'fuckult': fuckult.value,
        'theDate': date
    }
    return requests.get(f"{url}", params=params, timeout=1)
