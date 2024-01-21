import telebot, logging
from Ilkhom.keyboards.inline.inline_menu import menu_btn, types_btn
from Ilkhom.utils.util import content_type_media
from data import config
from telebot import types
from Ilkhom.db_config.db_postgresql import Database

db = Database()
db.create_user_table()
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


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    if call.data == 'en':
        test = call.message.chat.id
        echo = bot.send_message(test, 'What is your name?')
        bot.register_next_step_handler(echo, get_user_info)
        # bot.answer_callback_query(call.id, 'English')
    elif call.data == 'ru':
        bot.send_message(call.message.chat.id, 'Привет')
        # bot.answer_callback_query(call.id, 'Russian', show_alert=True)


def get_user_info(message):
    chat_id = message.chat.id
    name = message.text
    user_dict[chat_id] = User(name)
    echo = bot.send_message(chat_id, 'What is your age?')
    bot.register_next_step_handler(echo, get_age_info)


def get_age_info(message):
    chat_id = message.chat.id
    age = message.text
    if not age.isdigit():
        echo = bot.reply_to(message, text='Age should be a number. How old are you?')
        bot.register_next_step_handler(echo, get_age_info)
        return

    user = user_dict[chat_id]
    user.age = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = markup.add('Male', 'Female')
    echo = bot.send_message(chat_id, 'What is your gender?', reply_markup=btn)
    bot.register_next_step_handler(echo, get_sex_info)


def get_sex_info(message):
    chat_id = message.chat.id
    sex = message.text
    user = user_dict[chat_id]
    user.sex = sex
    bot.send_message(chat_id, f"Nice to meet you {user.name}\n Age: {user.age} \n Sex: {user.sex}👍")
    check_id = db.check_user_id(chat_id)
    print(check_id)

    if db.check_user_id(chat_id):
        user_name = user.name
        user_age = user.age
        user_sex = user.sex
        db.insert_user(chat_id, user_name, user_age, user_sex)


@bot.message_handler(content_types=content_type_media)
def bot_echo(msg):
    chat_id = msg.chat.id
    bot.copy_message(chat_id, chat_id, msg.id)


# db.close_db()

bot.infinity_polling(skip_pending=True)