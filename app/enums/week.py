from datetime import datetime
from enum import Enum

from app.data.convert import week_correction


class Week(Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'

    @staticmethod
    def today():
        return Week[datetime.today().strftime('%A').lower()]

    def next(self):
        cls = self.__class__

        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]


class UnderAboveWeek(Enum):
    under, above, all = range(3)

    def next(self):
        if self == self.under:
            return self.above
        return self.under


class ThisNextWeek(Enum):
    this_week, next_week = range(2)

    def next(self):
        if self == self.this_week:
            return self.next_week
        return self.this_week

    def convert_week(self):
        if (datetime.today().isocalendar()[1] + week_correction + self.value) % 2 != 0:
            return UnderAboveWeek.under
        return UnderAboveWeek.above
