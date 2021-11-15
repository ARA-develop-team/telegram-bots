import telebot
from telebot import types
from config import TOKEN as token

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
    second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, "testing kb", reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="menu",
                              reply_markup=keyboardmain)

    if call.data == "first":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="1t", callback_data="1")
        rele2 = types.InlineKeyboardButton(text="2t", callback_data="2")
        rele3 = types.InlineKeyboardButton(text="3t", callback_data="3")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1, rele2, rele3, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="replaced text",
                              reply_markup=keyboard)

    elif call.data == "second":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="replaced text",
                              reply_markup=keyboard)

    elif call.data == "1" or call.data == "2" or call.data == "3":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
        keyboard3 = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
        keyboard3.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="last layer",
                              reply_markup=keyboard3)


if __name__ == "__main__":
    bot.polling(none_stop=True)
# import telebot
# import config
# import random
#
# from telebot import types
#
# bot = telebot.TeleBot(config.TOKEN)
#
#
# @bot.message_handler(commands=['start'])
# def welcome(message):
#     sti = open('static/welcome.webp', 'rb')
#     bot.send_sticker(message.chat.id, sti)
#
#     # keyboard
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("🎲 Рандомное число")
#     item2 = types.KeyboardButton("😊 Как дела?")
#
#     markup.add(item1, item2)
#
#     bot.send_message(message.chat.id,
#                      "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
#                          message.from_user, bot.get_me()),
#                      parse_mode='html', reply_markup=markup)
#
#
# @bot.message_handler(content_types=['text'])
# def lalala(message):
#     if message.chat.type == 'private':
#         if message.text == '🎲 Рандомное число':
#             bot.send_message(message.chat.id, str(random.randint(0, 100)))
#         elif message.text == '😊 Как дела?':
#
#             markup = types.InlineKeyboardMarkup(row_width=2)
#             item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
#             item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
#
#             markup.add(item1, item2)
#
#             bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
#         else:
#             bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == 'good':
#                 bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
#             elif call.data == 'bad':
#                 bot.send_message(call.message.chat.id, 'Бывает 😢')
#
#             # remove inline buttons
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
#                                   reply_markup=None)
#
#             # show alert
#             bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
#                                       text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
#
#     except Exception as e:
#         print(repr(e))
#
#
# # RUN
# bot.polling(none_stop=True)
#
#
#
# # @bot.message_handler(content_types=['text'])
# # def echo(message):
# #     local_time = time.strftime('%Y-%m-%d', time.localtime())
# #     bot.send_message(message.chat.id, local_time)
