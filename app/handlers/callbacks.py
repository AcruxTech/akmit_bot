from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.utils.functions import some_func
from app.states.AddHomework import AddHomework


async def call_add_homework(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(date=call.data.split('_')[2])
    await state.set_state(AddHomework.enter_title)
    await call.message.answer('Введите название предмета')
    await call.answer()


async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Команда отменена')
    await state.finish()
    await call.answer()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_cancel, text='cancel', state='*')
    dp.register_callback_query_handler(call_add_homework, Text(startswith='add_homework'), state='*')
