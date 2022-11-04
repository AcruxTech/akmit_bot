from aiogram.dispatcher.filters.state import State, StatesGroup


class AddHomework(StatesGroup):
    enter_title = State()
