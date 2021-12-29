from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStates(StatesGroup):
    GROUP = State()
    SUBGROUP = State()
    REG = State()
