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
