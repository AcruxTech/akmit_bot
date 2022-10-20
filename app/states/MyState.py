from aiogram.dispatcher.filters.state import State, StatesGroup


class MyState(StatesGroup):
    a = State()
    b = State()