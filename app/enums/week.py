from datetime import datetime
from enum import Enum

from app.data.convert import week_correction
from app.enums import NextMixin


class Week(NextMixin, Enum):
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


class UnderAboveWeek(NextMixin, Enum):
    under, above, all = range(3)


class ThisNextWeek(NextMixin, Enum):
    this_week, next_week = range(2)

    def convert_week(self):
        if (datetime.today().isocalendar()[1] + week_correction + self.value) % 2 != 0:
            return UnderAboveWeek.under
        return UnderAboveWeek.above
