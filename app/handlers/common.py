from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.utils.keyboards import get_start_keyboard
from db.models.user import User
from db.models.group import default_group


async def start(message: types.Message):
    session = message.bot.get('db')

    with session.begin() as session:
        new_user = User(name = message.forward_sender_name, group_id = default_group.id)
        session.add(new_user)
    await message.answer('start', reply_markup=get_start_keyboard())


async def help(message: types.Message):
    await message.answer('/start - начать работу\n/help - доступные команды\n/cancel - отменить команду')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer('Команда отменена')
    await state.finish()


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(help, commands='help', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')