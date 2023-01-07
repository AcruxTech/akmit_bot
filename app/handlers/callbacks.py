from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy.orm import Session

from app.utils.functions import some_func
from app.states.AddHomework import AddHomework

from db.models.group import Group
from db.models.user import User
from db.models.lesson import Lesson

from common.variables import engine


async def call_add_homework(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(date=call.data.split('_')[2])
    await state.set_state(AddHomework.enter_title)
    await call.message.answer('Введите название предмета')
    await call.answer()


async def call_get_homework(call: types.CallbackQuery):
    print(call.data.split('_')[2])

    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=call.from_user.id).first()
        lessons: list[Lesson] = s.query(Lesson).filter_by(group_id=me.group_id).all()
        
    print(lessons[0])
    await call.message.answer('см cmd')


async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Команда отменена')
    await state.finish()
    await call.answer()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_add_homework, Text(startswith='add_homework'), state='*')
    dp.register_callback_query_handler(call_get_homework, Text(startswith='get_homework'), state='*')
    dp.register_callback_query_handler(call_cancel, text='cancel', state='*')
