from pyrogram import Client, filters
import pyrogram
from pyrogram.errors import FloodWait, MessageNotModified

import time
from time import sleep
import subprocess
import gallery
import threading
import select
import sys
import yaml


def config_parser(session=None, get_data=False, first_time=None):   # working with session.yml
    if get_data is True:        # output yaml
        with open('session.yml', 'r') as file:
            data_yml = yaml.load(file, yaml.Loader)

            if not data_yml:
                data_yml = "RECORDED SESSION ARE ABSENT"

            print(data_yml)

    elif session:     # saving session
        with open('session.yml', 'a') as file:

            end_time = time.strftime("%X", time.localtime())
            name_session = f'%s --> %s' % (first_time, end_time)
            building_data = {}

            for message in session:
                building_data[f'%s %s' % (message[4], message[0])] = f'"%s"  |  %s %s' % \
                                                                     (message[1], message[2], message[3])

            current_session = {name_session: building_data}
            yaml.dump(current_session, file, default_flow_style=False)


def send_message():
    active = threading.currentThread()
    while getattr(active, "do_run", True):
        i, o, e = select.select([sys.stdin], [], [], 2)        # timeout input (for closing thread)

        if i:
            entering = sys.stdin.readline().strip()

            if entering[0] == '^':       # requests

                if entering == '^get data':
                    config_parser(get_data=True)

                else:
                    print('info:\n^get data  -  to open session archive')

            else:        # sending message
                id_chat, message, id_indicator = '', '', True

                for symbol in entering:       # split id and message
                    if id_indicator is True:
                        if symbol == " ":
                            id_indicator = False
                        else:
                            id_chat += symbol
                    else:
                        message += symbol

                try:
                    app.send_message(id_chat, message)

                except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
                    print('[WRONG ID]')

                except pyrogram.errors.exceptions.bad_request_400.UsernameInvalid:
                    print('[WRONG USERNAME]')


print(f"Hello from the ARA!\n")
start_time = time.ctime()

app = Client("my_account")

sender = threading.Thread(target=send_message)
sender.start()

messages = []    # for saving session


@app.on_message(filters.command("art", prefixes=".") & filters.all)
def art(_, msg):
    try:
        picture = msg.text.split(".art ", maxsplit=1)[1]

    except IndexError:
        picture = None

    img = gallery.picture_stock(picture)
    try:
        msg.edit(img)

    except pyrogram.errors.exceptions.bad_request_400.MessageIdInvalid:
        app.send_message(msg['chat']['id'], img)


@app.on_message(filters.command("run", prefixes=".") & filters.all)
def run_program(_, msg):
    output_bytes = subprocess.check_output(['python3', 'gallery.py'])

    try:
        output = output_bytes.decode('utf-8')

        try:
            msg.edit(output)
        except pyrogram.errors.exceptions.bad_request_400.MessageIdInvalid:
            app.send_message(msg['chat']['id'], output)

    except AttributeError:
        app.send_message(msg['chat']['id'], "output data has AttributeError")

    except pyrogram.errors.exceptions.bad_request_400.MessageEmpty:
        app.send_message(msg['chat']['id'], "output data has MessageEmpty")


@app.on_message(filters.command("time", prefixes=".") & filters.me)
def get_time(_, msg):
    time_visual = True

    while time_visual:
        try:
            msg.edit(time.strftime("Time  %X", time.localtime()))  # %H:%M
            sleep(0.1)

        except FloodWait as e:
            sleep(e.x)

        except MessageNotModified:
            sleep(1)


@app.on_message(filters.command("close", prefixes=".") & filters.me)
def stop_terminal(_, msg):
    sender.do_run = False
    sender.join()
    config_parser(session=messages, first_time=start_time)
    msg.edit("Closing successfully completed")
    quit()


@app.on_message()  # must be the last func
def interception(_, msg):
    try:
        orig_text = msg.text.split(maxsplit=0)[0]
        if msg["chat"]["title"] is None:
            new_mess = (msg["from_user"]["first_name"], orig_text, msg["chat"]["first_name"],
                        msg["chat"]["id"], msg["message_id"])

            messages.append(new_mess)
            print(">>>  %s  -  %s               (%s) %s" % (new_mess[0], new_mess[1], new_mess[2], new_mess[3]))

        elif msg["from_user"] is None:
            new_mess = (msg["sender_chat"]["username"], orig_text, msg["chat"]["title"],
                        msg["chat"]["id"], msg["message_id"])

            messages.append(new_mess)
            print(">>>  %s  -  %s               (%s) %s" % (new_mess[0], new_mess[1], new_mess[2], new_mess[3]))

        else:
            new_mess = (msg["from_user"]["first_name"], orig_text, msg["chat"]["title"],
                        msg["chat"]["id"], msg["message_id"])

            messages.append(new_mess)
            print(">>>  %s  -  %s               (%s) %s" % (new_mess[0], new_mess[1], new_mess[2], new_mess[3]))

    except AttributeError:
        pass


app.run()

# @app.on_message(filters.private)
# async def hello(client, message):
# await message.reply_text(f"Hello {message.from_user.mention}")
# @app.on_message(filters.command("motion", prefixes=".") & filters.me)
# def loading_animation(_, msg):
#     while True:
#         for x in range(0, 8):
#             load_list = ["_", "_", "_", "_", "_", "_", "_", "_"]
#             load_list[x] = "-"
#             result = ''
#             for symbol in load_list:
#                 result += symbol
#
#             msg.edit(result)
#             sleep(1)

# from pyrogram.types import ChatPermissions
