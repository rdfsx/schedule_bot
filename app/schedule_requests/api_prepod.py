import asyncio
import random
from typing import Optional, List

from bs4 import BeautifulSoup, ResultSet

from app.data.convert import university_time, lessons_emoji
from app.enums.week import Week, ThisNextWeek
from app.schedule_requests.api import API
from app.enums.schedule import FuckultSchedule, Sem

from datetime import datetime

from app.utils.db_api.commands.commands_teacher import select_all_teachers


class APIMethodsPrepod:
    def __init__(self, prepod: str, fuckult: FuckultSchedule, api_: Optional[API] = None):
        self.api = api_ or API()
        self.prepod = prepod
        self.fuckult = fuckult

    async def __get_prepod_html(self,
                                sem: Sem,
                                date: Optional[str] = datetime.now().strftime('%Y-%m-%d')) -> str:
        params = {
            'prepod': f"'{self.prepod}'",
            'sem': sem.value,
            'fuckult': self.fuckult.value,
            'theDate': date,
            'brouser': 'Opera'
        }
        return await self.api.request("get/getRaspByPrepod", params)

    async def __get_timetable(self) -> ResultSet:
        sem = Sem.get_sem()
        text = await self.__get_prepod_html(sem)
        soup = BeautifulSoup(text, 'html.parser')
        return soup.find_all('td')

    async def __get_prepod_rows(self) -> list:
        lessons: list = []
        week_str = ThisNextWeek.this_week.convert_week()
        timetable = await self.__get_timetable()
        for td in timetable:
            try:
                title = td['title']
            except KeyError:
                continue
            text = " ".join(td.get_text().split())
            title_list = title.split(" ")
            date_num = [s for s in title_list if "~" in s][0]
            lesson_num = int(date_num.split("~")[1])
            kind = [s for s in title_list if "l" in s][0]
            date = date_num.split("~")[0]
            kind_str = '(лекц)' if int(kind.replace("l", "")) == 1 else '(практ)'
            month = int(date.split(".")[1].lstrip("0"))
            day = int(date.split(".")[0].lstrip("0"))
            day_week = datetime(datetime.now().year, month, day).strftime('%A').lower()
            result: List[str] = []
            week: str = ''
            if td['rowspan'] == '#':
                if (week_str.name == "under" and 'tp' in title) or (week_str.name == "above" and 'bt' in title):
                    week = "<b>На этой неделе:</b>"
                else:
                    week = "<b>На следующей неделе:</b>"
                if not text:
                    text = ""
                result.append(f"{text}")
            elif td['rowspan'].isdigit():
                if text:
                    for i in range(int(td['rowspan'])):
                        result.append(text)
            else:
                continue
            if result:
                for lesson in result:
                    lessons.append(
                        {
                            'lesson': lesson_num,
                            'date': date,
                            'week': week,
                            'day_week': day_week,
                            'kind_str': kind_str,
                            'text': lesson
                        }
                    )
        return lessons

    async def get_prep_schedule(self) -> list:
        lessons = await self.__get_prepod_rows()
        days = set([dic["day_week"] for dic in lessons if dic["day_week"] in list(map(lambda d: d.name, Week))])
        today = Week.today()
        sorted_days: list = []
        result: list = []
        for i in range(len(Week)):
            if today.name in days:
                sorted_days.append(today.name)
            today = today.next()
        for day in sorted_days:
            lessons_day = [dictionary for dictionary in lessons if dictionary["day_week"] == day]
            result.append(f"<b>{Week[lessons_day[0]['day_week']].value.title()} {lessons_day[0]['date']}</b>")
            for les in lessons_day:
                if les['text']:
                    result.append(f"{lessons_emoji.get(les['lesson'])}{les['week']} <i>{les['kind_str']}</i> "
                                  f"{les['text']} "
                                  f"<i><u>{university_time.get(les['lesson'])}</u></i>")
                else:
                    result.append(f"{lessons_emoji.get(les['lesson'])}{les['week']} Нет пары.")
        return result

    # async def compare_all_teachers(self):
    #     teachers = await select_all_teachers(limit=None)
    #
    # async def __get_prepods_list_string(self, sem: Sem) -> str:
    #     params = {
    #         'getPrepod': '1',
    #         'letters': '',
    #         'brouser': 'Opera',
    #         'GRU3': 'undefined',
    #         'sem': sem.value,
    #     }
    #     return await self.api.request("validList/ajaxGetList", params)
    #
    # async def get_prepods_list(self) -> List[str]:
    #     sem = Sem.get_sem()
    #     self.prepods_list = (await self.__get_prepods_list_string(sem)).replace("\ufeff", '').split("|")
    #     return self.prepods_list


async def main():
    schedule = await APIMethodsPrepod("Авакян Е.З.", FuckultSchedule.df).get_prep_schedule()
    for row in schedule:
        print(row)
    # schedule = await APIMethodsPrepod().get_prepods_list()
    # print(schedule)

asyncio.run(main())
