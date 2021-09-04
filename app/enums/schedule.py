from datetime import datetime
from enum import Enum


class FuckultSchedule(Enum):
    zf = 'zf'
    df = 'df'

    def next(self):
        return self.zf if self == self.df else self.df


class Sem(Enum):
    summer = 'summer'
    winter = 'winter'

    def next(self):
        return self.summer if self == self.winter else self.winter

    @staticmethod
    def get_sem():
        date = datetime.today()
        if datetime(month=1, day=24, year=date.year) <= date < datetime(month=6, day=30, year=date.year):
            return Sem.summer
        else:
            return Sem.winter
