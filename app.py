import telebot
from telebot import types
from extensions import Converter, APIException


#TODO база данный по субтитрам

TOKEN = "5156928592:AAHs5egCtuMoEZl7xxyg3yRI0iQtSU4XfQo"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    mess = f"{message.from_user.first_name}"
    bot.reply_to(message, "У тебя красивый голос, " + mess)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message) -> None:
    """
    The method handles two commands: '/start' and '/help' and gives the invitation.
    """
    text = "Ask the bot to convert currency: Use '/buttons' command to switch to buttons mode,"
        #or enter '/values' command to send request in the following format:
        #<amount> <base currency> to <target currency>.'"""
    bot.send_message(message.chat.id, text, parse_mode='html')
    
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message) -> None:
    text = "Values command received."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['buttons'])
def handle_buttons(message: telebot.types.Message) -> None:
    text = "Buttons command received."
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    button1 = types.KeyboardButton('button1')
    button2 = types.KeyboardButton('button2')
    markup.add(button1, button2)
    
    markup.add(types.InlineKeyboardButton('Currency', url='www.yandex.ru'))
    bot.send_message(message.chat.id, text, reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def handle_convert(message):
    pass


bot.polling(none_stop=True)