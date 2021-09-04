from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    GROUP = State()
    SUBGROUP = State()
    REG = State()
