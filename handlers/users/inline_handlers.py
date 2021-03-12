import hashlib
import random

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from aiogram.utils.markdown import hbold, hitalic

from data.convert import ERROR, PREPODS, sticker
from data.messages import donuts
from keyboards.inline.callback_datas import day_week_inline, teacher_inline, delete_teacher_rating, other_week_inline, \
    teacher_schedule
from keyboards.inline.inline_buttons import check_week, get_rating_kb, get_group_buttons, search_kb, teacher_schedule_kb
from loader import dp
from models.week import Week, ThisNextWeek
from states import States
from utils.db_api.commands.commands_teacher import select_all_teachers, set_rating, select_teacher_id, delete_rating
from utils.db_api.commands.commands_timetable import get_some_day, select_rows_by_teacher
from utils.db_api.commands.coomands_group import select_groups_limit, select_group_id
from utils.db_api.schemas.user import User


@dp.callback_query_handler(day_week_inline.filter())
async def get_other_group(call: CallbackQuery, user: User, callback_data: dict):
    group = user.group_id
    subgroup = user.subgroup
    day = Week[str(callback_data.get('day'))]
    week = ThisNextWeek[str(callback_data.get('this_or_next'))]
    week_text = 'следующей' if week == ThisNextWeek.next_week else 'этой'
    initial_message = f"{day.value.title()} на {week_text} неделе"
    txt = await get_some_day(day, group, week, subgroup, initial_message)
    await call.answer(initial_message)
    await call.message.edit_text(txt, reply_markup=(check_week(week, day)))


@dp.inline_handler(text_contains='#p')
async def get_teachers(inline_query: InlineQuery):
    limit = 20
    offset = 0 if inline_query.offset == '' else int(inline_query.offset)
    results = []
    data = await select_all_teachers(inline_query.query.replace('#p', ''), offset, limit)
    if data:
        for teacher in data:
            if teacher.count == 0:
                description = 'Пока нет оценок.'
            else:
                description = f"{round(teacher.rating / teacher.count, 1)}/5, количество оценок: {teacher.count}"
            results.append(InlineQueryResultArticle(
                id=str(hashlib.md5(teacher.full_name.encode()).hexdigest()),
                title=teacher.full_name,
                input_message_content=InputTextMessageContent(teacher.full_name),
                description=description,
                thumb_url=random.choice(PREPODS))
            )

    else:
        not_found = 'Нет такого преподавателя'
        results = [InlineQueryResultArticle(
            id=str(hashlib.md5(not_found.encode()).hexdigest()),
            title=not_found,
            input_message_content=InputTextMessageContent(not_found),
            thumb_url=ERROR)
        ]
    next_offset = str(offset + limit) if len(data) >= limit else ''
    await inline_query.answer(results=results, cache_time=60, next_offset=next_offset)


@dp.inline_handler()
async def get_groups(inline_query: InlineQuery):
    limit = 20
    offset = 0 if inline_query.offset == '' else int(inline_query.offset)
    results = []
    data = await select_groups_limit(inline_query.query, offset, limit)
    if data:
        for group in data:
            results.append(InlineQueryResultArticle(
                id=str(group.id),
                title=group.group,
                input_message_content=InputTextMessageContent(group.group),
                )
            )
    else:
        not_found = 'Нет такой группы'
        results = [InlineQueryResultArticle(
            id=str(hashlib.md5(not_found.encode()).hexdigest()),
            title=not_found,
            input_message_content=InputTextMessageContent(not_found),
            thumb_url=ERROR)
        ]
    next_offset = str(offset + limit) if len(data) >= limit else ''
    await inline_query.answer(results=results, next_offset=next_offset)


@dp.callback_query_handler(other_week_inline.filter())
async def get_other_schedule(call: CallbackQuery, callback_data: dict):
    group_id = str(callback_data.get('group_id'))
    group = await select_group_id(int(group_id))
    week = ThisNextWeek[str(callback_data.get('this_or_next'))]
    day = Week[str(callback_data.get('day'))]
    week_text = 'следующей' if week == ThisNextWeek.next_week else 'этой'
    day_txt = day.value.title()
    result_message = [hbold(f"{day_txt} на {week_text} неделе у группы {group.group}")]
    for i in range(1, group.subgroups + 1):
        initial_message = f"{i} подгруппа"
        result_subgroup = await get_some_day(day, group.id, week, i, initial_message)
        result_message.append(result_subgroup)
    await call.answer(f"{day_txt} на {week_text} неделе")
    await call.message.edit_text(('\n\n'.join(result_message)), reply_markup=get_group_buttons(week, group.id, day))


@dp.callback_query_handler(teacher_inline.filter())
async def set_rating_teacher(call: CallbackQuery, user: User, callback_data: dict):
    teacher_id = str(callback_data.get('teacher_id'))
    rating = str(callback_data.get('rating'))
    await set_rating(int(teacher_id), user.id, int(rating))
    teacher = await select_teacher_id(int(teacher_id))
    txt = [hbold(f"{teacher.full_name}")]
    rate = round(teacher.rating / teacher.count, 1)
    txt.append(hitalic(f"Вы поставили {rating}\nРейтинг: {rate}/5, количество оценок: {teacher.count}"))
    await call.answer('Рейтинг обновлён.')
    await call.message.edit_text('\n\n'.join(txt), reply_markup=get_rating_kb(teacher.id, str(user.id), True))


@dp.callback_query_handler(delete_teacher_rating.filter())
async def delete_teacher_rating_func(call: CallbackQuery, user: User, callback_data: dict):
    teacher_id = str(callback_data.get('teacher_id'))
    await delete_rating(int(teacher_id), user.id)
    teacher = await select_teacher_id(int(teacher_id))
    txt = [hbold(f"{teacher.full_name}\n")]
    if teacher.count == 0:
        txt.append(hitalic('Вы отменили оценку.\nПока что у преподавателя нет оценок.'))
    else:
        rate = round(teacher.rating / teacher.count, 1)
        txt.append(f"Вы отменили оценку.\nРейтинг: {rate}/5, количество оценок: {teacher.count}")
    await call.answer('Рейтинг обновлён.')
    await call.message.edit_text('\n'.join(txt), reply_markup=get_rating_kb(teacher.id, str(user.id), False))


@dp.callback_query_handler(teacher_schedule.filter())
async def get_teacher_schedule(call: CallbackQuery, callback_data: dict):
    teacher_id = str(callback_data.get('teacher_id'))
    week = ThisNextWeek[str(callback_data.get('this_or_next'))]
    week_text = 'следующей' if week == ThisNextWeek.next_week else 'этой'
    teacher = await select_teacher_id(int(teacher_id))
    teacher_name = teacher.full_name
    text = await select_rows_by_teacher(int(teacher_id), f'{teacher_name} на {week_text} неделе', week)
    await call.answer()
    await call.message.answer("\n\n".join(text), reply_markup=teacher_schedule_kb(week, int(teacher_id)))


@dp.callback_query_handler(text='sticker')
async def send_sticker(call: CallbackQuery):
    await call.answer()
    await call.message.answer_sticker(sticker=sticker)


@dp.callback_query_handler(text='donuts')
async def send_donut(call: CallbackQuery):
    await call.answer()
    await call.message.answer(donuts)


@dp.callback_query_handler(text='reset')
async def reset_user(call: CallbackQuery):
    await call.answer('Настройки сброшены.')
    await States.GROUP.set()
    await call.message.answer('Найдите свою группу:', reply_markup=search_kb)
