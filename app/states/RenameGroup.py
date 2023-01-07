from aiogram.dispatcher.filters.state import State, StatesGroup


class RenameGroup(StatesGroup):
    enter_title = State()
