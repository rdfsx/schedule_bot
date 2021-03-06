from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.convert import to_eng
from keyboards.inline.callback_datas import day_week_inline, other_week_inline, teacher_inline, teacher_schedule, \
    delete_teacher_rating, group_subgroups
from models.week import ThisNextWeek, Week

kb_more = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сброс настроек', callback_data='reset')
        ],
        [
            InlineKeyboardButton(text='Стикер с расписанием звонков', callback_data='sticker')
        ],
        [
            InlineKeyboardButton(text='Рейтинг преподавателей', switch_inline_query_current_chat='#p ')
        ],
        [
            InlineKeyboardButton(text='Чужое расписание', switch_inline_query_current_chat='')
        ],
    ]
)

search_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Найти', switch_inline_query_current_chat='')
        ]
    ]
)

search_teacher = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Рейтинг преподавателей', switch_inline_query_current_chat='#p ')
        ]
    ]
)

cancel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)


def get_rating_kb(teacher_id: str, user_id: str, rating_exist: bool = False) -> InlineKeyboardMarkup:
    buttons = []
    if rating_exist:
        buttons.append(
            InlineKeyboardButton(
                text='Удалить/изменить оценку',
                callback_data=delete_teacher_rating.new(
                    user_id=user_id,
                    teacher_id=teacher_id)
            )
        )
    else:
        for i in range(1, 6):
            buttons.append(
                InlineKeyboardButton(
                    text=str(i),
                    callback_data=teacher_inline.new(
                        user_id=user_id,
                        teacher_id=teacher_id,
                        rating=str(i)
                    )
                )
            )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons,
            [
                InlineKeyboardButton(
                    text='Расписание преподавателя',
                    callback_data=teacher_schedule.new(teacher_id=teacher_id, this_or_next=ThisNextWeek.this_week.name))
            ],
            [
                InlineKeyboardButton('Рейтинг преподавателей', switch_inline_query_current_chat='#p ')
            ]
        ]
    )


def get_group_buttons(week: ThisNextWeek, group: int, day: Week) -> InlineKeyboardMarkup:
    week_text = 'Следующая' if week == week.this_week else 'Текущая'
    buttons = []
    for i in ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'):
        buttons.append(
            InlineKeyboardButton(
                text=i,
                callback_data=other_week_inline.new(
                    day=to_eng.get(i.lower()),
                    this_or_next=week.name,
                    group_id=str(group)
                )
            )
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons,
            [
                InlineKeyboardButton(
                    text=f"{week_text} неделя",
                    callback_data=other_week_inline.new(
                        day=day.name,
                        this_or_next=week.next().name,
                        group_id=str(group)
                    )
                )
            ]
        ]
    )


def check_week(week: ThisNextWeek, day: Week) -> InlineKeyboardMarkup:
    week_text = 'Следующая' if week == week.this_week else 'Текущая'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{week_text} неделя",
                    callback_data=day_week_inline.new(
                        day=day.name,
                        this_or_next=week.next().name)
                )
            ]
        ]
    )


def teacher_schedule_kb(week: ThisNextWeek, teacher_id: int) -> InlineKeyboardMarkup:
    week_text = 'Следующая' if week == week.this_week else 'Текущая'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{week_text} неделя",
                    callback_data=teacher_schedule.new(
                        teacher_id=teacher_id,
                        this_or_next=week.next().name)
                )
            ]
        ]
    )


def subgroup_menu(num: int) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(num):
        sub = str(i + 1)
        keyboard.append(
            [
                InlineKeyboardButton(text=sub, callback_data=group_subgroups.new(number=sub)),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
