import asyncio
import collections
import operator
import random
import re
from typing import Optional, List, Any, Coroutine, Union

import bs4
from bs4 import BeautifulSoup, ResultSet

from data.convert import to_eng, to_rus, university_time, lessons_emoji
from models.lessons import LessonKind
from models.week import Week, ThisNextWeek, UnderAboveWeek
from schedule_requests.api import API
from models.schedule import FuckultSchedule, Sem

from datetime import datetime, timedelta

from schedule_requests.test_schr import group_list, groups
from utils.db_api.commands.commands_timetable import add_lesson, get_day_raw, get_all_schedule, select_all_rows, \
    delete_row, add_timetable
from utils.db_api.commands.coomands_group import select_all_groups, add_group, update_group, select_group


class APIMethodsGroup:
    def __init__(self, api_: Optional[API] = None):
        self.api = api_ or API()

    async def __get_timetable_html(self, groups: List[str], sem: Optional[Sem] = Sem.get_sem()) -> str:
        date = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        params = {
            'GRU': "','".join(groups),
            'sem': sem.value,
            'Type': 'Print',
            'theDate': date.strftime('%Y-%m-%d'),
            'brouser': 'Opera'
        }
        return await self.api.request("get/getRaspKaf", params)

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

    @staticmethod
    async def get_lessons_from_soup(element: bs4.element.Tag, groups_list: List[str]):
        try:
            title = element['title']
        except KeyError:
            return
        title_list = title.split(" ")
        try:
            group = str(re.findall(r'\?.+?\?', title)[0]).replace("?", '')
        except IndexError:
            return
        group_db = await select_group(group)
        if not group or not group_db:
            return
        try:
            quantity = int([s for s in title_list if "||" in s][0].split("||")[1])
        except IndexError:
            return
        quantity = 1 if quantity == 0 else quantity
        date_num = [s for s in title_list if "~" in s][0]
        date = date_num.split("~")[0]
        lesson_num = int(date_num.split("~")[1])
        month = int(date.split(".")[1].lstrip("0"))
        day = int(date.split(".")[0].lstrip("0"))
        day_week = Week[datetime(datetime.now().year, month, day).strftime('%A').lower()]
        text = " ".join(element.get_text().split())
        if not text:
            return
        subgroup: int = 0
        lesson_kind: LessonKind = LessonKind.lec
        if int(element['colspan']) > group_db.subgroups:
            i = group_db.subgroups
            j = 0
            while i <= int(element['colspan']):
                idx = groups_list.index(group) + j
                if idx > len(groups_list):
                    break
                gr = groups_list[idx]
                gr_info = await select_group(gr)
                i += gr_info.subgroups
                if i <= int(element['colspan']):
                    quantity += 1
                j += 1
        elif int(element['colspan']) == 0:
            lesson_kind = LessonKind.lec
        elif group_db.subgroups != int(element['colspan']):
            lesson_kind = LessonKind.lab
            subgroup = 1 if 'pr' in title else 2
        else:
            lesson_kind = LessonKind.lec if 'l1' in title else LessonKind.prac
        if element['rowspan'] == '#':
            week = UnderAboveWeek.under if 'tp' in title else UnderAboveWeek.above
        else:
            week = UnderAboveWeek.all
        group_idx = groups_list.index(group)
        result: List[List] = []
        for i in range(group_idx, group_idx + quantity):
            result.append([day_week, lesson_num, week, groups_list[i], subgroup, text, lesson_kind])
        return result

    @staticmethod
    def compare_rows(row1: list, row2: list) -> bool:
        return row1 == row2

    async def compare_all_groups(self):
        groups_from_request = group_list  # await self.get_all_groups()
        actual_groups_timetable = groups  # await self.__get_timetable_html(groups_from_request)
        db_groups_timetable = select_all_rows()
        soup = BeautifulSoup(actual_groups_timetable, 'html.parser')
        async for db_row in db_groups_timetable:
            have = False
            for td in soup.find_all('td'):
                print(td)
                if not td.get_text():
                    td.decompose()
                    continue
                request_rows = await self.get_lessons_from_soup(td, groups_from_request)
                if not request_rows:
                    td.decompose()
                    continue
                if db_row[1] in request_rows:
                    request_rows.remove(db_row[1])
                    have = True
                if not request_rows:
                    td.decompose()
            if not have:
                await delete_row(db_row[0])
        for td in soup.find_all('td'):
            request_rows = await self.get_lessons_from_soup(td, groups_from_request)
            if request_rows:
                for row in request_rows:
                    await add_timetable(*row)
                    print(row)

# wtf = ClientGroup("ИС-41")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(wtf.wtf())
# loop.close()
