import asyncio
import random
from typing import Optional, List

from bs4 import BeautifulSoup, ResultSet

from data.convert import to_eng, to_rus, university_time, lessons_emoji
from models.week import Week, ThisNextWeek
from schedule_requests.api import API
from models.schedule import FuckultSchedule, Sem

from datetime import datetime


class APIMethodsPrepod:
    def __init__(self, prepod: str, api_: Optional[API] = None):
        self.api = api_ or API()
        self.prepod = prepod

    async def __get_prepod_html(self,
                                sem: Sem,
                                fuckult: FuckultSchedule,
                                date: Optional[str] = datetime.now().strftime('%Y-%m-%d')) -> str:
        params = {
            'prepod': f"'{self.prepod}'",
            'sem': sem.value,
            'fuckult': fuckult.value,
            'theDate': date,
            'brouser': 'Opera'
        }
        return await self.api.request("get/getRaspByPrepod", params)

    async def __get_timetable(self) -> ResultSet:
        text: str = ''
        sem = Sem.get_sem()
        fuckult = FuckultSchedule.df
        for i in range(2):
            text += await self.__get_prepod_html(sem, fuckult)
            fuckult = fuckult.next()
            await asyncio.sleep(round(random.uniform(1, 3), 2))
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
                    result.append(f"{lessons_emoji.get(les['lesson'])}{les['week']} <b>{les['kind_str']}</b> "
                                  f"{les['text']} "
                                  f"<i><u>{university_time.get(les['lesson'])}</u></i>")
                else:
                    result.append(f"{lessons_emoji.get(les['lesson'])}{les['week']} Нет пары.")
        return result
