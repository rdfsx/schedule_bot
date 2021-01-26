import asyncio
import random
import re
from typing import Optional, List

from bs4 import BeautifulSoup, ResultSet

from data.convert import to_eng, to_rus, university_time, lessons_emoji
from models.week import Week, ThisNextWeek
from schedule_requests.api import API
from models.schedule import FuckultSchedule, Sem

from datetime import datetime, timedelta

from utils.db_api.commands.commands_timetable import add_lesson
from utils.db_api.commands.coomands_group import select_all_groups


class ClientGroup:
    def __init__(self, api_: Optional[API] = None):
        self.api = api_ or API()

    async def __get_timetable_html(self, groups: str, sem: Sem) -> str:
        date = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        params = {
            'GRU': groups,
            'sem': sem.value,
            'Type': 'Print',
            'theDate': date.strftime('%Y-%m-%d'),
            'brouser': 'Opera'
        }
        return await self.api.request("get/getRaspKaf", params)

    async def __get_all_groups_html(self) -> str:
        sem = Sem.get_sem()
        params = {
            'sem': sem.value,
            'brouser': 'Opera'
        }
        return await self.api.request("nazn/select", params)

    @staticmethod
    async def __get_all_groups_str(groups: List[str]) -> str:
        result = "','".join(groups)
        return f"'{result}'"

    async def get_all_groups(self) -> list:
        groups = await self.__get_all_groups_html()
        soup = BeautifulSoup(groups, 'html.parser')
        groups_list: list = []
        for li in soup.find_all('li'):
            text = " ".join(li.get_text().split())
            groups_list.append(text)
        return groups_list

    async def __get_groups_timetable(self, group: str):
        sem = Sem.get_sem()
        groups_list = await self.get_all_groups()
        groups_str = await self.__get_all_groups_str(groups_list)
        text = await self.__get_timetable_html(groups_str, sem)
        result_raw = []
        soup = BeautifulSoup(text, 'html.parser')
        for td in enumerate(soup.find_all('td')):
            try:
                title = td[1]['title']
            except KeyError:
                continue
            if td[1].get_text() == group:
                if td[1]['colspan'] == '1':
                    one_subgroup = True
            title_list = title.split(" ")
            try:
                target_group = [s for s in title_list if "?" in s][0]
                group1 = str(re.findall(r'\?.+?\?', target_group)[0]).replace("?", '')
                quantity_groups = int([s for s in title_list if "||" in s][0].split("||")[1])
            except IndexError:
                continue
            if quantity_groups > 1:
                if groups_list.index(group1) < groups_list.index(group) < groups_list.index(group1) + quantity_groups:
                    result_raw.append(td[1])
            if group in title:
                result_raw.append(td[1])

    async def get_timetable(self):
        pass

    async def __get_group_rows(self):
        pass

    async def get_group_timetable(self):
        pass

    async def compare_group(self):
        pass

    async def compare_all_groups(self):
        groups = await select_all_groups()
        for group in groups:
            timetable = await get_timetable(group)





    async def update_group_timetable(self):
        pass





# wtf = ClientGroup("ИС-41")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(wtf.wtf())
# loop.close()
