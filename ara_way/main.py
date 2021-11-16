"""ARA IN THE WAY!"""

import telebot
import config
from datetime import datetime
from client import Client

bot = telebot.TeleBot(config.TOKEN)
clients = {}
menus = config.build_menu()


def get_time():
    """Gets current time and converts to a list of ints
    :return: list of integers, string of current time
    """
    current_time_str = datetime.now().strftime("%H:%M")
    current_time_str_list = current_time_str.split(':')

    current_time = []
    for element in current_time_str_list:
        current_time.append(int(element))

    return current_time, current_time_str


@bot.message_handler(commands=['start'])
def welcome(message):
    """Processing of new user.
    :param message: message, which user sent
    """

    # keyboard
    main_menu = menus['main_menu']

    # new user
    is_new_user = True
    for user in clients:
        print(user)
        if user == message.chat.id:  # user.chat_ip
            is_new_user = False
            bot.send_message(message.chat.id,
                             "Bot is already working", reply_markup=main_menu)

    if is_new_user:
        clients[message.chat.id] = Client(message.chat.id)
        print(type(clients[message.chat.id]))
        bot.send_message(message.chat.id,
                         "Welcome {0.first_name}! \nARA_Way ^v^".format(message.from_user),
                         parse_mode='html', reply_markup=main_menu)


@bot.message_handler(commands=['price'])
def set_custom_price(message):
    section_message = (message.text.split(" "))
    try:
        section_price = float(section_message[1])

    except ValueError:
        bot.send_message(message.chat.id, 'Wrong syntax. Example: 14.50')

    else:
        user = clients[message.chat.id]
        last_road_data = user.last_road
        user.add_to_total(section_price)

        if last_road_data:
            bot.send_message(message.chat.id, f"Your road successfully saved😊  \nPrice: {section_price}€\n"
                                              f"Time: {last_road_data[2]} minutes")
            user.last_road = None

        else:
            bot.send_message(message.chat.id, f"You add {section_price}€ for your Total")


@bot.message_handler(content_types=['text'])
def command_handler(message):
    """Handler for commands from user.
    :param message: message, which user sent
    """

    if message.chat.type == 'private' and clients:
        user = clients[message.chat.id]

        if message.text == 'Start the road':
            if user.start_road_time is None:
                road_menu = menus['add_road']

                current_time, current_time_str = get_time()
                bot.send_message(message.chat.id, f"Start of the Road: {current_time_str}", reply_markup=road_menu)
                user.start_road_time = current_time

            else:
                bot.send_message(message.chat.id, "You haven’t finished your previous road")

        if message.text == 'Show Total':
            total = user.total
            bot.send_message(message.chat.id, 'Your Total: %s€' % total)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Creation multi-level inline menu."""

    if clients:
        if call.data == 'end':
            user = clients[call.message.chat.id]
            current_time, _ = get_time()
            road_time = user.count_time(current_time)

            prices = list(user.count_price(road_time))
            user.last_road = [*prices, road_time]

            price_menu = menus['prices']
            price_menu.__dict__['keyboard'][0][0]['text'] = f"{prices[0]}€"
            price_menu.__dict__['keyboard'][0][1]['text'] = f"{prices[1]}€"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Spent time: {road_time} minutes\nChoose the price:", reply_markup=price_menu)

        elif call.data == 'discount' or call.data == 'no_discount':
            user = clients[call.message.chat.id]
            last_road_data = user.last_road
            price = last_road_data[1] if call.data == 'discount' else last_road_data[0]
            user.add_to_total(price)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Your road successfully saved😊  \nPrice: {price}€\n"
                                       f"Time: {last_road_data[2]} minutes")
            user.last_road = None

        elif call.data == 'road_cancel':
            confirm_menu = menus['sure']
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Are you sure you want to cancel the road?", reply_markup=confirm_menu)

        elif call.data == 'yes':
            clients[call.message.chat.id].start_road_time = None
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Road has been cancelled")

        elif call.data == 'no':
            road_menu = menus['add_road']
            start_time = "{}:{}".format(*clients[call.message.chat.id].start_road_time)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Start of the Road: {start_time}", reply_markup=road_menu)

        elif call.data == 'custom_price':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Custom price, input example:\n/price 14.50")


if __name__ == '__main__':
    bot.polling(none_stop=True)
