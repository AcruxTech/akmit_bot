from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.utils.functions import some_func
from app.states.CreateGroup import CreateGroup


async def call_add_homework(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(some_func(2))
    await state.set()
    await call.answer()


async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Команда отменена')
    await state.finish()
    await call.answer()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_cancel, text='cancel', state='*')
    dp.register_message_handler(call_add_homework, Text(startswith='add_homework'), state='*')
