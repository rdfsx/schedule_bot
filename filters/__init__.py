from aiogram import Dispatcher

from .is_admin import AdminFilter
from .is_day import DayFilter
from .is_group import GroupFilter
from .is_teacher import TeacherFilter
from .is_registered import RegisterFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(DayFilter)
    dp.filters_factory.bind(GroupFilter)
    dp.filters_factory.bind(TeacherFilter)
    dp.filters_factory.bind(RegisterFilter)
