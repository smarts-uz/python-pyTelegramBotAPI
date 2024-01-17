import telebot
from Ilkhom.keyboards.inline.inline_menu import menu_btn
from Ilkhom.utils.util import content_type_media
from telebot import types
from data import config

bot = telebot.TeleBot(token=config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, text='Assalomu alaykum')
    bot.send_message(msg.chat.id, text='Please select language', reply_markup=menu_btn)




@bot.message_handler(content_types=content_type_media)
def bot_echo(msg):
    chat_id = msg.chat.id
    bot.copy_message(chat_id, chat_id, msg.id)




bot.infinity_polling()