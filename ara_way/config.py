"""TRAVEL BOT DATA"""
from telebot import types

TOKEN = '2136122286:AAHtrdjZtm7U9RhPIO8S5QcjL4M0uYdykak'
admin_id = 694236273


def build_menu():
    menus = {}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Start the road")
    item2 = types.KeyboardButton("Show Total")
    item3 = types.KeyboardButton("--Travel pass--")
    item4 = types.KeyboardButton("--Optional--")
    markup.add(item1, item2, item3, item4)

    inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="End the road", callback_data='end')
    item2 = types.InlineKeyboardButton(text="Cancel", callback_data='road_cancel')
    inline.add(item1, item2)

    inline2 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Yes", callback_data='yes')
    item2 = types.InlineKeyboardButton(text="No", callback_data='no')
    inline2.add(item1, item2)

    inline3 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="without discount", callback_data='no_discount')
    item2 = types.InlineKeyboardButton(text="with discount", callback_data='discount')
    item3 = types.InlineKeyboardButton(text="Custom", callback_data='custom_price')
    inline3.add(item1, item2, item3)

    # markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for button in range(1, 10):
    #     item = types.InlineKeyboardButton(text=f"{button}", callback_data=f'${button}')
    #     markup2.add(item)
    # item1 = types.KeyboardButton(text="Ok", callback_data='$ok')
    # item2 = types.KeyboardButton(text="0", callback_data='$0')
    # item4 = types.KeyboardButton(text="Del")
    # markup2.add(item1, item2, item3, item4)

    menus['main_menu'] = markup
    menus['add_road'] = inline
    menus['sure'] = inline2
    menus['prices'] = inline3

    return menus
