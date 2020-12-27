from aiogram.utils.markdown import hbold, hitalic

from asyncpg import UniqueViolationError, NotNullViolationError

from sqlalchemy import func, select, and_, text

from data.convert import lessons_emoji, university_time
from models.week import UnderAboveWeek, Week, ThisNextWeek

from utils.db_api.db_gino import db
from utils.db_api.schemas.group import Groups
from utils.db_api.schemas.schedule import Timetable, Lessons


async def add_lesson(lesson: str):
    try:
        await Lessons(lesson=lesson).create()

    except UniqueViolationError:
        pass


async def add_timetable(day_week: Week, lesson_num: int, week: UnderAboveWeek, group: str, subgroup: int, lesson: str):
    try:
        timetable = Timetable(
            day_week=day_week,
            lesson_num=lesson_num,
            week=week,
            group_id=await Groups.select('id').where(Groups.group == group).gino.scalar(),
            subgroup=subgroup,
            lesson_id=await Lessons.select('id').where(Lessons.lesson == lesson).gino.scalar()
        )
        await timetable.create()

    except NotNullViolationError:
        pass


async def get_some_day(day: Week, group: int, week: ThisNextWeek, subgroup: int, initial_message: str = ''):
    timetable = await get_day_raw(day, group, subgroup, week)
    if not timetable:
        return hbold(f"{initial_message}:\n\nНет пар!")
    message = [hbold(f"{initial_message}:")]
    for lesson in timetable:
        emoji = lessons_emoji.get(lesson[0])
        lesson_value = lesson[1]
        lesson_time = f"<i><u>{university_time.get(lesson[0])}</u></i>"
        message.append(f"{emoji} {lesson_value} {lesson_time}")
    return '\n\n'.join(message)


async def get_day_raw(day: Week, group: int, subgroup: int, week: ThisNextWeek = ThisNextWeek.this_week):
    week = week.convert_week()
    join = Timetable.join(Lessons)
    statement = select([Timetable.lesson_num, Lessons.lesson]).select_from(join)
    condition = statement \
        .where(Timetable.day_week == day.name) \
        .where(Timetable.week == week.name) \
        .where(Timetable.group_id == group) \
        .where(Timetable.subgroup == subgroup)
    return await condition.order_by(Timetable.lesson_num).gino.all()


async def check_existence(day: Week, group: int, week: ThisNextWeek, subgroup: int) -> bool:
    return await db.scalar(
        db.exists()
        .where(Timetable.day_week == day.name)
        .where(Timetable.week == week.convert_week())
        .where(Timetable.group_id == group)
        .where(Timetable.subgroup == subgroup).select()
    )
