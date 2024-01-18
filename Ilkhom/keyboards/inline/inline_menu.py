from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu_btn():
    menu = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='EN', callback_data='en'),
        InlineKeyboardButton(text='RU', callback_data='ru')
    ]])

    return menu


def types_btn():
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(InlineKeyboardButton(text='EN', callback_data='en'), InlineKeyboardButton(text='RU', callback_data='ru'))
    # menu.insert(InlineKeyboardButton(text='EN', callback_data='en'))
    # menu.insert(InlineKeyboardButton(text='RU', callback_data='ru'))
    return menu
