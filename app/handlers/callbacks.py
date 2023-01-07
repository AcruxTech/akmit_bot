from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy.orm import Session

from app.states.AddHomework import AddHomework
from app.states.RenameGroup import RenameGroup

from db.models.user import User
from db.models.lesson import Lesson

from common.variables import engine
from common.constants import NO_HW_TEXT


async def call_group_change_title(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите новое название для группы')
    await state.set_state(RenameGroup.enter_title.state)
    await call.answer()


async def call_group_show_members(call: types.CallbackQuery, state: FSMContext):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=call.from_user.id).first()
        members: list[User] = s.query(User).filter_by(group_id=me.group_id).all()

    text = 'Участники:\n\n'
    for i, member in enumerate(members):
        text += f'{i + 1}. <i>{member.name}</i>\n'

    await call.message.answer(text, parse_mode='HTML')
    await call.answer()


async def call_group_leave(call: types.CallbackQuery, state: FSMContext):
    with Session(engine) as s:
        s.query(User).filter(User.uuid == call.from_user.id).update(
            {'group_id': None}, 
            synchronize_session='fetch'
        )
        s.commit()

    await call.message.answer('Вы вышли из группы :(')
    await call.answer()


async def call_add_homework(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(date=call.data.split('_')[2])
    await state.set_state(AddHomework.enter_title)
    await call.message.answer('Введите название предмета')
    await call.answer()


async def call_get_homework(call: types.CallbackQuery):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=call.from_user.id).first()
        lessons: list[Lesson] = s.query(Lesson).filter_by(
            group_id=me.group_id,
            date=call.data.split('_')[2]
        ).all()

    text = ''
    if not len(lessons):
        text = NO_HW_TEXT

    for i, lesson in enumerate(lessons):
        text += f'<i>Предмет</i>: <b>{lesson.title}</b>\n<i>Д/з</i>: {lesson.homework}\n'
        if i != len(lessons) - 1:
            text += '---------\n'
    
    await call.message.answer(text, parse_mode='HTML')
    await call.answer()


async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Команда отменена')
    await state.finish()
    await call.answer()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_group_change_title, Text('group_change_title'), state='*')
    dp.register_callback_query_handler(call_group_show_members, Text('group_show_members'), state='*')
    dp.register_callback_query_handler(call_group_leave, Text('group_leave'), state='*')
    dp.register_callback_query_handler(call_add_homework, Text(startswith='add_homework'), state='*')
    dp.register_callback_query_handler(call_get_homework, Text(startswith='get_homework'), state='*')
    dp.register_callback_query_handler(call_cancel, text='cancel', state='*')
