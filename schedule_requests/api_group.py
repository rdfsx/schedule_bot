import asyncio
import random
import re
from typing import Optional, List, Any, Coroutine, Union

import bs4
from bs4 import BeautifulSoup, ResultSet

from data.convert import to_eng, to_rus, university_time, lessons_emoji
from models.week import Week, ThisNextWeek, UnderAboveWeek
from schedule_requests.api import API
from models.schedule import FuckultSchedule, Sem

from datetime import datetime, timedelta

from utils.db_api.commands.commands_timetable import add_lesson, get_day_raw, get_all_schedule
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
        group = str(re.findall(r'\?.+?\?', title)[0]).replace("?", '')
        group_db = await select_group(group)
        if not group or not group_db:
            return
        quantity = int([s for s in title_list if "||" in s][0].split("||")[1])
        quantity = 1 if quantity == 0 else quantity
        date_num = [s for s in title_list if "~" in s][0]
        date = date_num.split("~")[0]
        lesson_num = date_num.split("~")[1]
        month = int(date.split(".")[1].lstrip("0"))
        day = int(date.split(".")[0].lstrip("0"))
        day_week = datetime(datetime.now().year, month, day).strftime('%A').lower()
        text = " ".join(element.get_text().split())
        subgroup: int = 0
        if group_db.subgroups != int(element['colspan']):
            text += "<i>(лаб.)</i>"
            subgroup = 1 if 'pr' in title else 2
        else:
            text += "<i>(лекц.)</i>" if 'l1' in title else "<i>(практ.)</i>"
        if element['rowspan'] == '#':
            week = UnderAboveWeek.under if 'tp' in title else UnderAboveWeek.above
        else:
            week = UnderAboveWeek.all
        group_idx = groups_list.index(group)
        result: List[dict] = [{}]
        for i in range(group_idx, group_idx + quantity):
            result.append(
                dict(day_week=day_week,
                     lesson_num=lesson_num,
                     week=week,
                     subgroup=subgroup,
                     group=groups_list[i],
                     lesson=text)
            )
        return result


    async def __get_groups_timetable(self, group: str):
        sem = Sem.get_sem()
        groups_list = await self.get_all_groups()
        groups_timetable = await self.__get_all_groups_str(groups_list)
        text = await self.__get_timetable_html(groups_timetable, sem)
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
            if quantity_groups > 1 and groups_list.index(group1) < groups_list.index(group) < groups_list.index(
                    group1) + quantity_groups:
                result_raw.append(td[1])
            if group in title:
                result_raw.append(td[1])

    async def get_timetable(self, timetable_soup, group: str, group_list: List[str],
                            count: int = 0):
        td = timetable_soup.find('td')
        title: Union[str, Any] = ''
        try:
            title = td['title']
        except KeyError:
            td.decompose()
            await self.get_timetable(timetable_soup, group, group_list)
        if td.get_text() == group:
            if int(td['colspan']) == 1:
                one_subgroup = True
        title_list = title.split(" ")
        target_group: str
        try:
            target_group = [s for s in title_list if "?" in s][0]
            target_group = str(re.findall(r'\?.+?\?', target_group)[0]).replace("?", '')
            quantity_groups = int([s for s in title_list if "||" in s][0].split("||")[1])
            if quantity_groups > 1 and group_list.index(target_group) < group_list.index(group) < group_list.index(
                    target_group) + quantity_groups:
                result_raw.append(td[1])
            if group in title:
                result_raw.append(td[1])
        except IndexError:
            td.decompose()
            await self.get_timetable(timetable_soup, group, group_list)

    async def update_group(self, actual_timetable: List[List[str]], db_timetable: List[List[str]]):
        for lesson in actual_timetable:
            pass

    async def compare_all_groups(self):
        groups_from_db = await select_all_groups()
        groups_from_request = await self.get_all_groups()
        groups_timetable = self.__get_timetable_html(groups_from_request)
        soup = BeautifulSoup(groups_timetable, 'html.parser')
        for group in groups_from_db:
            actual_timetable = sorted(await self.get_timetable(soup, group, groups_from_request))
            db_timetable = sorted(await get_all_schedule(group))
            if actual_timetable != db_timetable:
                await self.update_group(actual_timetable, db_timetable)






    async def update_group_timetable(self):
        pass





# wtf = ClientGroup("ИС-41")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(wtf.wtf())
# loop.close()