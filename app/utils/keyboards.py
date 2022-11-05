from aiogram import types

from common.constants import DAYS


def get_add_homework_keyboard() -> types.InlineKeyboardMarkup:
    from datetime import date, timedelta

    today = date.today()
    buttons = []
    for i in range(7):
        t = today + timedelta(days=i)
        text = f'{t.day}.{t.month}.{str(t.year)[2:]}'
        buttons.append(types.InlineKeyboardButton(text=f'{text} ({DAYS[t.weekday()]})', callback_data=f'add_homework_{text}'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
