import telebot
from pathlib import Path
from src.config import *
from src.email_creator import Creator, Messages


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    with open(Path('src/files/welcome_message.txt'), 'r') as f:
        welcoming_text = f.read()
    bot.send_sticker(message.chat.id, STICKER_ID)
    bot.reply_to(message, welcoming_text)


@bot.message_handler(commands=['new_email'])
def new_email(message):
    creator = Creator()
    try:
        token = creator.create_account()

        global messages
        messages = Messages(token)

        email, password = creator.get_email(), creator.get_pass()
        reply = f'Account was created!\nEmail: {email}\nPassword: {password}'
    except:
        reply = 'Sorry, there are problem with creating account!'
    bot.reply_to(message, reply)


@bot.message_handler(commands=['get_all_messages_id'])
def get_all_messages(message):
    try:
        my_messages = messages.get_messages_id()
        if my_messages == []:
            reply = 'Sorry, there are no messages.'
        else:
            reply = f'Your messages:\n{my_messages}'
    except:
        reply = 'Sorry, there are problem with getting messages id!'
    bot.reply_to(message, reply)


@bot.message_handler(commands=['get_last_message'])
def get_last_message(message):
    try:
        messages.form_last_message_info()
        reply = reply_former(messages)
    except:
        reply = 'Sorry, there are no messages.'
    bot.reply_to(message, reply)


@bot.message_handler(commands=['sub_to_message'])
def sub_to_message(message):
    control = True
    while control:
        try:
            messages.form_last_message_info()
            reply = reply_former(messages)
            bot.reply_to(message, reply)
            control = False
        except:
            pass


@bot.message_handler(func=lambda message: True)
def get_message(message):
    try:
        messages.form_message_info(message.text)
        reply = reply_former(messages)
    except:
        reply = f'Sorry, there are no message with id "{message.text}".'
    bot.reply_to(message, reply)


# inner function
def reply_former(messages):
    reply = \
f'Sender\'s email: {messages.get_email()}\n\
Sender\'s name: {messages.get_name()}\n\
Subject: {messages.get_subject()}\n\
Text: {messages.get_text()}'
    return reply


def main():
    bot.infinity_polling()
