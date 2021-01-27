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

from utils.db_api.commands.commands_timetable import add_lesson, get_day_raw, get_all_schedule
from utils.db_api.commands.coomands_group import select_all_groups


class APIMethodsGroup:
    def __init__(self, api_: Optional[API] = None):
        self.api = api_ or API()
        self.groups_list_db: List[str] = asyncio.run(select_all_groups())
        self.groups_list_gstu: List[str] = asyncio.run(self.get_all_groups())

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

    async def __get_all_groups_str(self) -> str:
        result = "','".join(self.groups_list_db)
        return f"'{result}'"

    async def get_all_groups(self) -> list:
        sem = Sem.get_sem()
        params = {
            'sem': sem.value,
            'brouser': 'Opera'
        }
        groups = await self.api.request("nazn/select", params)
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

    async def get_timetable(self, group: str):
        return [["wtf"]]

    async def __get_group_rows(self):
        pass

    async def get_group_timetable(self):
        pass

    @staticmethod
    async def compare_group(actual_timetable: List[List[str]], db_timetable: List[List[str]]) -> bool:
        actual_timetable.sort()
        db_timetable.sort()
        return True if actual_timetable == db_timetable else False

    async def update_group(self):
        pass

    async def compare_all_groups(self):
        for group in self.groups_list_gstu:
            actual_timetable = await self.get_timetable(group)
            db_timetable = await get_all_schedule(group)
            await APIMethodsGroup.compare_group(actual_timetable, db_timetable)






    async def update_group_timetable(self):
        pass





wtf = APIMethodsGroup()


loop = asyncio.get_event_loop()
loop.run_until_complete(wtf.get_all_groups_str())
loop.close()