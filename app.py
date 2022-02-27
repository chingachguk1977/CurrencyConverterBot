import telebot
from config import codes_human
from telebot import types
from extensions import Converter, APIException


#TODO база данный по субтитрам

TOKEN = "5156928592:AAHs5egCtuMoEZl7xxyg3yRI0iQtSU4XfQo"

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=False, resize_keyboard=True)
buttons = []
for code, name in codes_human.items():
    buttons.append(types.KeyboardButton(code.upper()))

markup.add(*buttons)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message) -> None:
    """
    The method handles two commands: '/start' and '/help' and gives the invitation.
    """
    text = "Ask the bot to convert currency."
    bot.send_message(message.chat.id, text, parse_mode='html')
    
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message) -> None:
    text = 'Available currencies:'
    for code, name in codes_human.items():
        text = '\n'.join(text, code, name[1])
    bot.send_message(message.chat.id, text)
    
@bot.message_handler(commands=['convert'])
def handle_convert(message):
    text = "Choose the (base) currency to convert from:"
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, source_handler)
    
def source_handler(message):
    source = message.text.strip()
    text = "Now choose the (target) currency to convert into:"
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, target_handler, source)
    
def target_handler(message, source):
    target = message.text.strip()
    text = "Now type the amount of your base currency:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, conv_handler, source, target)
    
def conv_handler(message, source, target):
    amount = message.text.strip()
    try:
        result_amount = Converter.get_price(source, target, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Conversion error: \n{e}\nTry again.")
        
    else:
        text = f"{amount} {codes_human[source][0]} = {result_amount} {codes_human[target][0]}."
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def handle_convert(message):
    pass


bot.polling(none_stop=True)