from aiogram import types
from datetime import date, timedelta


def get_days_keyboard(callback: str) -> types.InlineKeyboardMarkup: 
    buttons = []
    for i in range(7):
        today = date.today() + timedelta(days=i)
        str_today = today.strftime('%d.%m.%y')
        buttons.append(
            types.InlineKeyboardButton(f'{str_today} ({today.strftime("%a").lower()})', 
            callback_data=callback + str_today)
        )
    return types.InlineKeyboardMarkup().add(*buttons)


def get_group_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton('Изменить название', callback_data='group_change_title'),
        types.InlineKeyboardButton('Показать участников', callback_data='group_show_members'),
        types.InlineKeyboardButton('Выйти из группы', callback_data='group_leave')
    ]
    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)
    return keyboard
