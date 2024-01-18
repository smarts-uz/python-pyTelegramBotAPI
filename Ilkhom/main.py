import telebot, logging
from Ilkhom.keyboards.inline.inline_menu import menu_btn, types_btn
from Ilkhom.utils.util import content_type_media
from data import config
from telebot import types

bot = telebot.TeleBot(token=config.BOT_TOKEN)
# telebot.logger.setLevel(logging.DEBUG)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, text='Welcome!')
    bot.send_message(msg.chat.id, text='Please select language:', reply_markup=types_btn())
    # echo = bot.send_message(msg.chat.id, text='What is your name?')
    # bot.register_next_step_handler(echo, get_user)


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    if call.data == 'en':
        bot.answer_callback_query(call.id, 'English')
    elif call.data == 'ru':
        bot.answer_callback_query(call.id, 'Russian', show_alert=True)


def get_user(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    echo = bot.reply_to(message, text='How old are you?')
    bot.register_next_step_handler(echo, get_age)


def get_age(message):
    chat_id = message.chat.id
    age = message.text
    if not age.isdigit():
        echo = bot.reply_to(message, text='Age should be a number. How old are you?')
        bot.register_next_step_handler(echo, get_age)
        return
    user = user_dict[chat_id]
    user.age = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = markup.add('Male', 'Female')
    echo = bot.send_message(chat_id, 'What is your gender?', reply_markup=btn)
    bot.register_next_step_handler(echo, get_sex)


def get_sex(message):
    chat_id = message.chat.id
    sex = message.text
    user = user_dict[chat_id]
    user.sex = sex
    bot.send_message(chat_id, f"Nice to meet you {user.name}\n Age: {user.age} \n Sex: {user.sex}👍")





# @bot.message_handler(content_types=content_type_media)
# def bot_echo(msg):
#     chat_id = msg.chat.id
#     bot.copy_message(chat_id, chat_id, msg.id)



bot.infinity_polling(skip_pending=True)