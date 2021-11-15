"""ARA IN THE WAY!"""

import telebot
import config
import time
from client import Client

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
clients, menus = {}, {}


def stopwatch(chat_id, message_id):
    passed_time = 0
    while True:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Road. Time: {passed_time}")


@bot.message_handler(commands=['start'])
def welcome(message):
    """Processing of new user.
    message: message, which user sent
    """

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Start the road")
    item2 = types.KeyboardButton("Show Total")
    item3 = types.KeyboardButton("Travel pass")
    item4 = types.KeyboardButton("Optional")
    markup.add(item1, item2, item3, item4)
    menus['mainmenu'] = markup

    # new user
    is_new_user = True
    for user in clients:
        print(user)
        if user == message.chat.id:    # user.chat_ip
            is_new_user = False
            bot.send_message(message.chat.id,
                             "Bot is already working", reply_markup=markup)

    if is_new_user:

        clients[message.chat.id] = Client(message.chat.id)
        print(type(clients[message.chat.id]))
        bot.send_message(message.chat.id,
                         "Welcome {0.first_name}! \nARA_Way ^v^".format(message.from_user),
                         parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def command_handler(message):
    """Handler for commands from user.
    message: message, which user sent
    """

    if message.chat.type == 'private' and clients:

        if message.text == 'Start the road':
            kb = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton(text="End the road", callback_data='end')
            item2 = types.InlineKeyboardButton(text="Cancel", callback_data='road_cancel')
            kb.add(item1, item2)
            bot.send_message(message.chat.id, "Road. Time: __:__", reply_markup=kb)

        if message.text == 'Show Total':
            print("working")
            total = clients[message.chat.id].total
            bot.send_message(message.chat.id, 'Your Total: %s' % total)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'end':
        price = 0.45   # ATTENTION!!!!
        clients[call.message.chat.id].addition(price)   # add cost of the ride to total
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Your road successfully saved😊  \nPrice: {price}€")


if __name__ == '__main__':
    bot.polling(none_stop=True)
