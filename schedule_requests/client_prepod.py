from typing import Optional

from bs4 import BeautifulSoup, ResultSet

from data.convert import to_eng, to_rus, university_time, lessons_emoji
from models.week import Week
from schedule_requests.api import API
from models.schedule import FuckultSchedule, Sem

from datetime import datetime


class ClientPrepod:
    def __init__(self, prepod: str, api_: Optional[API] = None):
        self.api = api_ or API()
        self.prepod = prepod

    def __get_html(self,
                   sem: Sem,
                   fuckult: FuckultSchedule,
                   date: Optional[str] = datetime.now().strftime('%Y-%m-%d')) -> str:
        params = {
            'prepod': f"'{self.prepod}'",
            'sem': sem.value,
            'fuckult': fuckult.value,
            'theDate': date
        }
        return self.api.request("get/getRaspByPrepod", params).text

    def __get_timetable(self) -> ResultSet:
        text: str = ''
        sem = Sem.summer
        fuckult = FuckultSchedule.df
        for i in range(2):
            for j in range(2):
                text += self.__get_html(sem, fuckult)
                fuckult = fuckult.next()
            sem = sem.next()
        soup = BeautifulSoup(text, 'html.parser')
        return soup.find_all('td')

    def __get_rows(self) -> list:
        day_week: str = ''
        lessons: list = []
        timetable = self.__get_timetable()
        for td in timetable:
            for key in to_eng.keys():
                if key in td.get_text().lower():
                    if to_eng[key] != '':
                        day_week = to_rus[key]
            try:
                title = td['title']
            except KeyError:
                continue
            title_list = title.split(" ")
            date_num = [s for s in title_list if "~" in s][0]
            kind = [s for s in title_list if "l" in s][0]
            kind_str = '(лекц)' if int(kind.replace("l", "")) == 1 else '(практ)'
            span = int(td['rowspan'])
            date = date_num.split("~")[0]
            lesson = int(date_num.split("~")[1])
            text = " ".join(td.get_text().split())
            if text:
                for i in range(span):
                    result = {
                        'lesson': lesson + i,
                        'date': date,
                        'day_week': day_week,
                        'kind_str': kind_str,
                        'text': text
                    }
                    lessons.append(result)
        return lessons

    def get_prep_schedule(self) -> list:
        lessons = self.__get_rows()
        days = set([dic["day_week"] for dic in lessons if dic["day_week"] in list(map(lambda d: d.value, Week))])
        today = Week.today()
        sorted_days: list = []
        result: list = []
        for i in range(len(Week)):
            if today.value in days:
                sorted_days.append(today.value)
            today = today.next()
        for day in sorted_days:
            lessons_day = [dictionary for dictionary in lessons if dictionary["day_week"] == day]
            result.append(f"<b>{lessons_day[0]['day_week'].title()} {lessons_day[0]['date']}</b>")
            for les in lessons_day:
                result.append(f"{lessons_emoji.get(les['lesson'])}<b>{les['kind_str']}</b> "
                              f"{les['text']} "
                              f"<i><u>{university_time.get(les['lesson'])}</u></i>")
        return result
