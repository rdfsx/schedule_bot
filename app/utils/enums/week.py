from datetime import datetime
from enum import Enum


class UnderAboveWeek(Enum):
    under, above = range(2)

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


class DayWeek(Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'

    monday_

    def next(self):
        cls = self.__class__

        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

    @staticmethod
    def today():
        return DayWeek[datetime.today().strftime('%A').lower()], ThisNextWeek.this_week

    @staticmethod
    def tomorrow():
        day = DayWeek[datetime.today().strftime('%A').lower()].next()
        week = ThisNextWeek.next_week if day == DayWeek.monday else ThisNextWeek.this_week
        return day, week


class Week:

    def __init__(self):
        self.today = self.today()
        self.tomorrow = self.tomorrow()

    @staticmethod
    def today():
        return DayWeek[datetime.today().strftime('%A').lower()], ThisNextWeek.this_week

    @staticmethod
    def tomorrow():
        day = DayWeek[datetime.today().strftime('%A').lower()].next()
        week = ThisNextWeek.next_week if day == DayWeek.monday else ThisNextWeek.this_week
        return day, week


wtf = Week()
print(wtf.today)
print(wtf.tomorrow)

