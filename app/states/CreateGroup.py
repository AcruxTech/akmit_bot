from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateGroup(StatesGroup):
    enter_title = State()
