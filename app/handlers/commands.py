from uuid import uuid4
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link, decode_payload
from sqlalchemy.orm import Session

from app.states.CreateGroup import CreateGroup
from app.states.RenameGroup import RenameGroup 
from app.states.AddHomework import AddHomework 
from app.utils.keyboards import get_days_keyboard, get_group_keyboard
from db.models.group import Group
from db.models.user import User
from db.models.lesson import Lesson

from common.variables import worker, engine
from common.constants import START_TEXT, HELP_TEXT, NOT_IN_GROUP_TEXT


async def start(message: types.Message):
    payload = decode_payload(message.get_args())
    group_id = int(payload) if payload != '' else None

    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()
        if me is None:
            new_user = User(
                uuid=message.from_user.id, 
                name = message.from_user.first_name, 
                group_id=group_id
            )
            s.add(new_user)
            s.commit()

    await message.answer(START_TEXT)


async def me(message: types.Message):
    group = ''

    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()
        if me.group_id is None:
            group = 'вне группы'   
        else: 
            group = s.query(Group).filter_by(id=me.group_id).first().title
        
    await message.answer(
        f'<i>Имя</i>: {me.name}\n<i>Название группы</i>: {group}',
        parse_mode='HTML'
    )
    

async def group(message: types.Message, state: FSMContext):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()
        
        if me.group_id is not None:
            group: Group = s.query(Group).filter_by(id=me.group_id).first()
            await message.answer(
                f'<i>Название</i>: {group.title}',
                parse_mode='HTML',
                reply_markup=get_group_keyboard()
            )
            return
        
    await message.answer('Вы не состоите в группе!\nВведите название для создания (потом можно изменить)')
    await state.set_state(CreateGroup.enter_title.state)


async def enter_title_group(message: types.Message, state: FSMContext):
    uuid = str(uuid4())

    # union into one session
    with Session(engine) as s:
        group = Group(uuid=uuid, title=message.text)
        s.add(group)
        s.commit()

    with Session(engine) as s:
        created_group: Group = s.query(Group).filter_by(uuid=uuid).first()
        s.query(User).filter(User.uuid == message.from_user.id).update(
            {'group_id': created_group.id}, 
            synchronize_session='fetch'
        )
        s.commit()

    await message.answer('Группа добавлена')
    await state.finish()


async def rename_group(message: types.Message, state: FSMContext):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()
        s.query(Group).filter(Group.id == me.group_id).update(
            {'title': message.text}, 
            synchronize_session='fetch'
        )
        s.commit()

    await message.answer('Группа успешно переименована')


async def generate_invite_link(message: types.Message):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()

    if me.group_id is None:
        await message.answer(NOT_IN_GROUP_TEXT)
        return

    link = await get_start_link(str(me.group_id), encode=True)
    await message.answer(f'Пригласительная ссылка в вашу группу: {link}')


async def add_homework(message: types.Message):
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()

    if me.group_id is None:
        await message.answer(NOT_IN_GROUP_TEXT)
        return
    await message.answer('Выберите дату', reply_markup=get_days_keyboard('add_homework_'))


# add keyboard with suggestions 
async def enter_title_homework(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Введите текст дз')
    await state.set_state(AddHomework.enter_homework)


async def enter_homework(message: types.Message, state: FSMContext):
    data = await state.get_data()

    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=message.from_user.id).first()
        lesson = Lesson(
            title = data['title'],
            homework = message.text,
            date = data['date'],                      
            group_id = me.group_id
        )
        s.add(lesson)
        s.commit()

    await message.answer('дз добавлено')
    await state.finish()


async def get_homework(message: types.Message):
    await message.answer('выберите день', reply_markup=get_days_keyboard('get_homework_'))


async def help(message: types.Message):
    await message.answer(HELP_TEXT)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer('Команда отменена')
    await state.finish()

# remove
async def clean(message: types.Message):
    worker.drop_all()
    await message.answer('db was cleaned')


async def unknown(message: types.Message):
    await message.answer('Неизвестная команда!')


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(me, commands='me', state='*')
    dp.register_message_handler(group, commands='group', state='*')
    dp.register_message_handler(enter_title_group, state=CreateGroup.enter_title)
    dp.register_message_handler(rename_group, state=RenameGroup.enter_title)
    dp.register_message_handler(generate_invite_link, commands='invite', state='*')
    dp.register_message_handler(add_homework, commands='add', state='*')
    dp.register_message_handler(enter_title_homework, state=AddHomework.enter_title)
    dp.register_message_handler(enter_homework, state=AddHomework.enter_homework)
    dp.register_message_handler(get_homework, commands='get_homework', state='*')
    dp.register_message_handler(help, commands='help', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')    

    # !
    dp.register_message_handler(clean, commands='clean', state='*')

    dp.register_message_handler(unknown, state='*')
    