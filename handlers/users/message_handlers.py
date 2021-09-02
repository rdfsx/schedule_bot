from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.utils.markdown import hbold, hitalic

from config import admins
from data.convert import to_rus
from data.messages import base_message
from filters import DayFilter, GroupFilter, TeacherFilter, RegisterFilter
from keyboards.default import menu
from keyboards.inline.callback_datas import message_for_admin
from keyboards.inline.inline_buttons import check_week, kb_more, get_group_buttons, get_rating_kb
from loader import dp, bot
from models.lessons import Lesson
from models.week import Week, ThisNextWeek
from utils.db_api.commands.commands_teacher import select_teacher_by_name, get_rating
from utils.db_api.commands.commands_timetable import get_some_day, check_existence, get_day_raw
from utils.db_api.commands.coomands_group import select_group, select_group_id
from utils.db_api.schemas.user import User
from aiogram.utils.markdown import quote_html


@dp.message_handler(TeacherFilter())
async def get_teacher(message: types.Message, user: User):
    teachers = await select_teacher_by_name(message.text)
    for teacher in teachers:
        txt = [
            hbold(f"{teacher.full_name}\n")]
        rating = await get_rating(teacher.id, user.id)
        if teacher.count == 0:
            txt.append(hitalic('Пока нет оценок. Вы можете быть первым!'))
        else:
            if rating:
                txt.append(hitalic(f"Вы поставили {rating.rate}"))
            rate = round(teacher.rating / teacher.count, 1)
            txt.append(hitalic(f"Рейтинг: {rate}/5, количество оценок: {teacher.count}"))
        await message.answer('\n'.join(txt),
                             reply_markup=get_rating_kb(teacher.id, str(user.id), True if rating else False))


@dp.message_handler(GroupFilter())
async def get_other_group(message: types.Message):
    week = ThisNextWeek.this_week
    group = await select_group(message.text)
    day = Week.monday
    result_message = [hbold(f"{day.value.title()} на этой неделе у группы {group.group}")]
    for i in range(1, group.subgroups + 1):
        initial_message = f"{i} подгруппа"
        result_subgroup = await get_some_day(day, group.id, week, i, initial_message)
        result_message.append(result_subgroup)
    await message.answer('\n\n'.join(result_message), reply_markup=get_group_buttons(week, group.id, day))


@dp.message_handler(RegisterFilter())
async def is_registered(message: types.Message):
    text = [
        "Вы не выбрали группу.",
        "Нажмите /start или /reset чтобы иметь возможность просматривать расписание.",
    ]
    await message.answer("\n".join(text))


@dp.message_handler(Text(equals=['сегодня', 'завтра'], ignore_case=True))
async def get_today_tomorrow(message: types.Message, user: User):
    day = Week.today() if message.text.casefold() == 'сегодня' else Week.today().next()
    subgroup = user.subgroup
    week = ThisNextWeek.this_week
    group = user.group_id
    initial_message = message.text.title()
    if Week.today() in (Week.saturday, Week.sunday):
        if not await check_existence(day, group, week, subgroup):
            initial_message = 'В понедельник на следующей неделе'
            week = week.next()
            day = Week.monday
    txt = await get_some_day(day, group, week, subgroup, initial_message)
    await message.answer(txt, reply_markup=menu)


@dp.message_handler(DayFilter())
async def get_day_week(message: types.Message, user: User):
    week = ThisNextWeek.this_week
    day = Week(to_rus.get(message.text.lower()))
    today = Week.today()
    group = user.group_id
    subgroup = user.subgroup
    initial_message = day.value.title()
    if today in (Week.saturday, Week.sunday):
        if not await check_existence(today, group, week, subgroup):
            initial_message += ' на следующей неделе'
            week = ThisNextWeek.next_week
    txt = await get_some_day(day, group, week, subgroup, initial_message)
    await message.answer(txt, reply_markup=(check_week(week, day)))


@dp.message_handler(Text('сейчас', ignore_case=True))
async def get_now(message: types.Message, user: User):
    week = ThisNextWeek.this_week
    day = Week.today()
    group = user.group_id
    subgroup = user.subgroup
    now = float(datetime.strftime(datetime.now(), "%H.%M"))
    schedule = await get_day_raw(day, group, subgroup, week)
    if not schedule:
        return await message.answer("Сегодня нет пар!", reply_markup=menu)
    if now > Lesson(schedule[-1][0]).to_float_list()[1]:
        return await message.answer("Сегодня больше не будет пар!", reply_markup=menu)
    now_lesson = ''
    next_lesson = ''
    if now < Lesson(schedule[0][0]).to_float_list()[0]:
        return await message.answer(
            hbold('Следующим:\n\n') +
            Lesson(schedule[0][0]).do_lesson_str(schedule[0][1], schedule[0][2], schedule[0][3]),
            reply_markup=menu
        )
    for num, lesson in enumerate(schedule):
        time = Lesson(lesson[0])
        time_tuple = time.to_float_list()
        if now > time_tuple[1]:
            continue
        begin = time_tuple[0]
        end = time_tuple[1]
        if begin <= now <= end:
            now_lesson = Lesson(lesson[0]).do_lesson_str(lesson[1], lesson[2], lesson[3])
            num += 1
        elif now < begin:
            now_lesson = "Премена"
        if num < len(schedule) and now_lesson:
            next_lesson = Lesson(schedule[num][0]).do_lesson_str(schedule[num][1], schedule[num][2], schedule[num][3])
            break
        elif now_lesson:
            next_lesson = "Сегодня больше не будет пар!"
            break
    txt = [
        hbold("Сейчас:"),
        now_lesson,
        hbold("Следующим:"),
        next_lesson
    ]
    await message.answer('\n\n'.join(txt), reply_markup=menu)


@dp.message_handler(Text(equals=['еще', 'ещё'], ignore_case=True))
async def get_more(message: types.Message, user: User):
    week = ThisNextWeek.this_week.convert_week()
    if not user.group_id:
        txt = ["Выберите действие:"]
    else:
        txt = [
            f'Сейчас неделя <b>{"над" if week == week.under else "под"}</b> чертой\n'
            f'Выбранная группа {hbold((await select_group_id(user.group_id)).group)}\n'
            f'Подгруппа: {hbold(user.subgroup)}',
        ]
    await message.answer('\n'.join(txt), reply_markup=kb_more)


@dp.message_handler(content_types=types.ContentType.ANY)
async def hot_handled(message: types.Message, user: User):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ответить',
                callback_data=message_for_admin.new(
                    from_user_id=message.from_user.id,
                    message_id=message.message_id
                )
            )
        ]
    ])
    for admin in admins:
        txt = [
            f'#message',
            f'Группа: {(await select_group_id(user.group_id)).group}',
            f'Имя: <a href="tg://user?id={message.from_user.id}">'
            f'{quote_html(message.from_user.full_name)}</a>',
            f"username: @{message.from_user.username}",
        ]
        if message.content_type == ContentType.TEXT:
            txt.append(f"\n{quote_html(message.text)}")
        else:
            txt.append(f"Content type: <u>{message.content_type}</u>")
            await message.send_copy(admin)
        await bot.send_message(admin, '\n'.join(txt), reply_markup=markup)
    await message.answer(base_message, reply_markup=menu)
