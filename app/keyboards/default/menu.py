from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='ПН'),
        KeyboardButton(text='ВТ'),
        KeyboardButton(text='СР'),
        KeyboardButton(text='ЧТ'),
        KeyboardButton(text='ПТ'),
        KeyboardButton(text='СБ')],
        [
        KeyboardButton(text='Сегодня'),
        KeyboardButton(text='Сейчас'),
        KeyboardButton(text='Завтра'),
        KeyboardButton(text='Ещё')
        ]],
    resize_keyboard=True)


def subgroup_menu(num: int) -> ReplyKeyboardMarkup:
    keyboard = []
    for i in range(num):
        keyboard.append([KeyboardButton(text=f"{i + 1}")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
