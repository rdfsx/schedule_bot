from contextlib import suppress
from typing import Optional, List

from aiogram.utils.markdown import hbold
from asyncpg import UniqueViolationError, NotNullViolationError
from sqlalchemy import select, or_

from app.enums.lessons import Lesson, LessonKind
from app.enums.week import UnderAboveWeek, Week, ThisNextWeek
from app.utils.db_api.commands.commands_teacher import select_teacher_id
from app.utils.db_api.commands.coomands_group import select_group_exact_match
from app.utils.db_api.db_gino import db
from app.utils.db_api.schemas.group import Groups
from app.utils.db_api.schemas.schedule import Timetable, Lessons
from app.utils.db_api.schemas.teacher import Teacher


async def add_lesson(lesson: str):
    with suppress(UniqueViolationError):
        await Lessons(lesson=lesson).create()


async def add_timetable(day_week: Week, lesson_num: int, week: UnderAboveWeek, group: str, subgroup: int, lesson: str,
                        lesson_kind: Optional[LessonKind] = None, teacher: Optional[int] = None):
    await add_lesson(lesson)
    try:
        timetable = Timetable(
            day_week=day_week,
            lesson_num=lesson_num,
            week=week,
            group_id=await Groups.select('id').where(Groups.group == group).gino.scalar(),
            subgroup=subgroup,
            lesson_id=await Lessons.select('id').where(Lessons.lesson == lesson).gino.scalar(),
            lesson_kind=lesson_kind,
            teacher_id=teacher,
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
        message.append(Lesson(lesson[0]).do_lesson_str(lesson[1], lesson[2], lesson[3]))
    return '\n\n'.join(message)


async def get_day_raw(day: Week, group: int, subgroup: int, week: ThisNextWeek = ThisNextWeek.this_week):
    calendar_week = week.convert_week()
    join = Timetable.join(Lessons).outerjoin(Teacher)
    stmt = select([Timetable.lesson_num, Lessons.lesson, Timetable.lesson_kind, Teacher.full_name]).select_from(join)
    condition = stmt \
        .where(Timetable.day_week == day.name) \
        .where(or_(Timetable.week == calendar_week.name, Timetable.week == calendar_week.all)) \
        .where(Timetable.group_id == group) \
        .where(or_(Timetable.subgroup == subgroup, Timetable.subgroup == 0))
    return await condition.order_by(Timetable.lesson_num).gino.all()


async def check_existence(day: Week, group: int, week: ThisNextWeek, subgroup: int) -> bool:
    return await db.scalar(
        db.exists()
        .where(Timetable.day_week == day.name)
        .where(Timetable.week == week.convert_week())
        .where(Timetable.group_id == group)
        .where(Timetable.subgroup == subgroup).select()
    )


async def select_all_rows(groups: List[str]):
    groups_id: List[int] = []
    for group_str in groups:
        group = await select_group_exact_match(group_str)
        groups_id.append(group.id)
    rows = [Timetable.id, Timetable.day_week, Timetable.lesson_num, Timetable.week, Groups.group, Timetable.subgroup,
            Lessons.lesson, Timetable.lesson_kind, Timetable.teacher_id]
    stmt = db.select(rows).select_from(Timetable.join(Lessons).join(Groups))
    for row in await stmt.where(Timetable.group_id.in_(groups_id)).gino.all():
        yield row.id, list(row)[1:]


async def select_by_teacher(teacher_id: int, week: ThisNextWeek = ThisNextWeek.this_week):
    week_calendar = week.convert_week()
    join = Timetable.join(Lessons).join(Groups)
    stmt = select([Timetable.lesson_num, Lessons.lesson, Timetable.lesson_kind, Groups.group, Timetable.day_week])\
        .select_from(join)
    condition = stmt \
        .where(or_(Timetable.week == week_calendar.name, Timetable.week == week_calendar.all)) \
        .where(Timetable.teacher_id == teacher_id)
    return await condition.order_by(Timetable.lesson_num).gino.all()


async def select_rows_by_teacher(teacher_id: int, initial_message: str, week: ThisNextWeek = ThisNextWeek.this_week) \
        -> List[str]:
    timetable = await select_by_teacher(teacher_id, week)
    teacher = await select_teacher_id(teacher_id)
    teacher_list = teacher.full_name.split(" ")
    teacher_initials = f"{teacher_list[0]} {teacher_list[1][0]}.{teacher_list[2][0]}."
    result = [hbold(f"{initial_message}:")]
    if not timetable:
        return [hbold(f"{initial_message}:\n\nНет пар.")]
    for day in Week:
        lessons_by_day = [list_ for list_ in timetable if list_[-1] == day]
        if lessons_by_day:
            result.append(f"<b>{lessons_by_day[0][4].value.title()}</b>")
            max_ = max([x[0] for x in lessons_by_day])
            min_ = min([x[0] for x in lessons_by_day])
            for i in range(min_, max_ + 1):
                lessons_num = [list_ for list_ in lessons_by_day if list_[0] == i]
                if lessons_num:
                    groups = [list_[3] for list_ in lessons_num]
                    lesson = Lesson(lessons_num[0][0])
                    result.append(f"{lesson.to_emoji()} <i>({lessons_num[0][2].value})</i> "
                                  f"{lessons_num[0][1]} <code>{teacher_initials}</code> <b>{', '.join(groups)}</b> "
                                  f"{lesson.to_time()}")
    return result


async def delete_row(row_id: int):
    return await Timetable.delete.where(Timetable.id == row_id).gino.status()
