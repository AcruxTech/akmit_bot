from aiogram import types
from datetime import date, timedelta


def get_add_homework_keyboard() -> types.InlineKeyboardMarkup: 
    buttons = []
    for i in range(7):
        today = date.today() + timedelta(days=i)
        str_today = today.strftime('%d.%m.%y')
        buttons.append(
            types.InlineKeyboardButton(f'{str_today} ({today.strftime("%a").lower()})', 
            callback_data=f'add_homework_{str_today}')
        )
    return types.InlineKeyboardMarkup().add(*buttons)
