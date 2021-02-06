import asyncio
import random

from loguru import logger

import re
from typing import Optional, List

import bs4
from bs4 import BeautifulSoup

from models.fuckult import Fuckult
from models.lessons import LessonKind
from models.week import Week, UnderAboveWeek
from schedule_requests.api import API
from models.schedule import Sem

from datetime import datetime, timedelta

from schedule_requests.fuuuck import fuck_timetable
from utils.admin_tools.admins_notify import notify_admins
from utils.db_api.commands.commands_teacher import select_teacher_by_name, add_teacher
from utils.db_api.commands.commands_timetable import select_all_rows, delete_row, add_timetable
from utils.db_api.commands.coomands_group import add_group, select_group


class APIMethodsGroup:
    def __init__(self, api_: Optional[API] = None):
        self.api = api_ or API()

    async def __get_timetable_html(self, groups: List[str], sem: Optional[Sem] = Sem.get_sem()) -> str:
        date = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        groups = "','".join(groups)
        params = {
            'GRU': f"'{groups}'",
            'sem': sem.value,
            'Type': 'Print',
            'theDate': date.strftime('%Y-%m-%d'),
            'brouser': 'Opera'
        }
        return await self.api.request("get/getRaspKaf", params, 10)

    async def get_all_groups(self) -> BeautifulSoup:
        sem = Sem.get_sem()
        params = {
            'sem': sem.value,
            'brouser': 'Opera'
        }
        groups = await self.api.request("nazn/getSort", params)
        soup = BeautifulSoup(groups, 'html.parser')
        return soup

    async def get_lessons_from_soup(self, element: bs4.element.Tag, groups_list: List[str]):
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
        teacher_id = await self.is_prepod_in_db(element.get_text())
        if teacher_id:
            text = "".join(element.get_text().replace("\t", "").strip().split("\n")[:-1])
        else:
            text = " ".join(element.get_text().split())
        if not text:
            return
        text = " ".join(text.split())
        subgroup: int = 0
        lesson_kind: LessonKind = LessonKind.lec
        colspan = int(element['colspan'])
        if colspan > group_db.subgroups:
            i = 0
            j = 0
            quantity = 0
            while i <= colspan:
                idx = groups_list.index(group) + j
                if idx >= len(groups_list):
                    break
                gr = groups_list[idx]
                gr_info = await select_group(gr)
                i += gr_info.subgroups
                if i <= colspan:
                    quantity += 1
                j += 1
        elif 0 < colspan < group_db.subgroups:
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
            result.append([day_week, lesson_num, week, groups_list[i], subgroup, text, lesson_kind, teacher_id])
        return result

    @staticmethod
    async def is_prepod_in_db(text: str) -> int:
        text = text.replace("\t", "").strip().split("\n")
        search_teacher = re.findall(r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.+[А-ЯЁ]\.", text[-1])
        if search_teacher:
            teacher = search_teacher[0]
            find_row = teacher.split(" ")
            find_teachers = await select_teacher_by_name(find_row[0])
            for available_teacher in find_teachers:
                teacher_split = available_teacher.full_name.replace(".", "").split(' ')
                teacher_initials = f"{teacher_split[0]} {teacher_split[1][0]}.{teacher_split[2][0]}."
                if teacher_initials == teacher:
                    return available_teacher.id
            return await add_teacher(teacher.replace(".", ". "))

    async def __compare_groups(self, groups_from_request: List[str]):
        actual_groups_timetable = await self.__get_timetable_html(groups_from_request)
        db_groups_timetable = select_all_rows(groups_from_request)
        soup = BeautifulSoup(actual_groups_timetable, 'html.parser')
        count_del = 0
        count_add = 0
        result_rows = []
        for td in soup.find_all('td'):
            text = "".join(td.get_text().split())
            if not text:
                td.decompose()
                continue
            elif text in groups_from_request:
                await add_group(text, Fuckult.FAIS, int(td['colspan']))
                td.decompose()
                continue
            request_rows = await self.get_lessons_from_soup(td, groups_from_request)
            if not request_rows:
                td.decompose()
                continue
            for row in request_rows:
                result_rows.append(row)
            td.decompose()
        async for db_row in db_groups_timetable:
            if db_row[1] in result_rows:
                result_rows.remove(db_row[1])
            else:
                await delete_row(db_row[0])
                count_del += 1
        if result_rows:
            for result_row in result_rows:
                await add_timetable(*result_row)
                count_add += 1
        return count_add, count_del

    async def compare_all_groups(self):
        sort_groups = await self.get_all_groups()
        logger.info("Starting schedule update.")
        for ul in sort_groups.find_all('ul'):
            groups_category = []
            for li in ul.find_all('li'):
                text = " ".join(li.get_text().split())
                groups_category.append(text)
            add, delete = await self.__compare_groups(groups_category)
            logger.info(f"Schedule update. {', '.join(groups_category)}: {add} rows added, {delete} rows deleted.")
            await notify_admins(f"Обновление расписания {', '.join(groups_category)}: добавлено {add} строк, "
                                f"удалено {delete}.")
            await asyncio.sleep(random.randint(5, 13))
        logger.info("Schedule is up-to-date.")
        await notify_admins("Расписание обновлено.")
