from datetime import datetime
from enum import Enum

from app.enums import NextMixin


class FuckultSchedule(NextMixin, Enum):
    zf = 'zf'
    df = 'df'
    mag_df = 'mag_df'
    mag_zf = 'mag'


class Sem(NextMixin, Enum):
    summer = 'summer'
    winter = 'winter'

    @staticmethod
    def get_sem():
        date = datetime.today()
        if datetime(month=1, day=24, year=date.year) <= date < datetime(month=6, day=30, year=date.year):
            return Sem.summer
        else:
            return Sem.winter
