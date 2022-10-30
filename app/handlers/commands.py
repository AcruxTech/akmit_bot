from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session

from app.utils.keyboards import get_start_keyboard
from db.models.user import User

# !
from common import worker, engine

async def start(message: types.Message):
    with Session(bind=engine) as s:
        me = s.query(User).filter_by(uuid=message.from_user.id).first()
        if me is None:
            new_user = User(uuid=message.from_user.id, name = message.from_user.first_name)
            s.add(new_user)
            s.commit()

    await message.answer('start', reply_markup=get_start_keyboard())
    

async def help(message: types.Message):
    await message.answer('/start - начать работу\n/help - доступные команды\n/cancel - отменить команду')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer('Команда отменена')
    await state.finish()


# !
async def clean(message: types.Message):
    worker.drop_all()
    await message.answer('db was cleaned')


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(help, commands='help', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')

    dp.register_message_handler(clean, commands='clean', state='*')
