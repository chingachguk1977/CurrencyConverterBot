import telebot
from config import codes_human
from telebot import types
from datetime import date
from extensions import Converter, APIException
from tkn import TOKEN


bot = telebot.TeleBot(TOKEN)

markup_codes = types.ReplyKeyboardMarkup(row_width=10, one_time_keyboard=True, resize_keyboard=False)
buttons = []
for code in codes_human.keys():
    buttons.append(types.KeyboardButton(code.upper()))
markup_codes.add(*buttons)

markup_numbers = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True, resize_keyboard=False)
numbers = ['1', '5', '10', '20', '50', '100', '200', '500', '1000']
markup_numbers.add(*numbers)

markup_commands = types.InlineKeyboardMarkup()
command1 = types.InlineKeyboardButton("Buttons mode", callback_data='switch_to_buttons')
command2 = types.InlineKeyboardButton("List of currencies", callback_data='show_available_currencies')
markup_commands.add(command1, command2)


@bot.callback_query_handler(func=lambda c: c.data == 'switch_to_buttons')
def on_error_buttons(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, '/buttons')

@bot.callback_query_handler(func=lambda c: c.data == 'show_available_currencies')
def on_error_buttons(callback_query: types.CallbackQuery):
    #bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, '/values')

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message) -> None:
    """
    The method handles two commands: '/start' and '/help' and gives the invitation.
    """
    text = """<b>The bot works in two modes:</b>
1. Text mode: just message the request in the following format: 
<b>amount source_currency target_currency</b>
For list of currencies, send the /values command. '1 GBP USD' will tell you the price of 1 GBP in USD.
2. Buttons mode:
Send the /convert or /buttons command. Type in the amount when the bot asks you to."""
    bot.send_message(message.chat.id, text, parse_mode='html')
    
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message) -> None:
    text = 'Available currencies:\n'
    for code, name in codes_human.items():
        text = ''.join((text, code+': ', name[1]+'\n'))
    bot.send_message(message.chat.id, text, reply_markup=markup_commands)
    
@bot.message_handler(commands=['convert', 'buttons'])
def handle_convert(message):
    text = "Choose the (base) currency to convert from:"
    bot.send_message(message.chat.id, text, reply_markup=markup_codes)
    bot.register_next_step_handler(message, source_handler)
    
def source_handler(message):
    source = message.text.strip()
    text = "Now choose the (target) currency to convert into:"
    bot.send_message(message.chat.id, text, reply_markup=markup_codes)
    bot.register_next_step_handler(message, target_handler, source)
    
def target_handler(message, source):
    target = message.text.strip()
    text = "Now choose the amount of your base currency or press a button:"
    bot.send_message(message.chat.id, text, reply_markup=markup_numbers)
    bot.register_next_step_handler(message, conv_handler, source, target)
    
def conv_handler(message, source, target):
    amount = message.text.strip()
    try:
        result_amount = Converter.get_price(source, target, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Conversion error: \n{e}\nTry again.", reply_markup=markup_commands)
    else:
        text = f'Today, {date.today().strftime("%B %d, %Y")}, \n'
        text += f'\n<b>{amount} {codes_human[source][0]} = {result_amount} {codes_human[target][0]}</b>.\n'
        text += f'\nData received from www.cbr.ru, Central Bank of Russia site: \
            <a>https://www.cbr.ru/currency_base/daily/</a>'
        bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(content_types=['text'])
def handle_text_conversion(message):
    
    try:
        msg = message.text.strip().upper().split()
        amount = msg[0]
        source = msg[1]
        target = msg[2]
        result_amount = Converter.get_price(source, target, amount)
    except IndexError:
        bot.send_message(message.chat.id, f"Conversion error.\nTry again.", reply_markup=markup_commands)
    except APIException as e:
        bot.send_message(message.chat.id, f"Conversion error: \n{e}\nTry again.", reply_markup=markup_commands)
    else:
        text = f'Today, {date.today().strftime("%B %d, %Y")}, \n'
        text += f'\n<b>{amount} {codes_human[source][0]} = {result_amount} {codes_human[target][0]}.</b>\n'
        text += f'\nData received from www.cbr.ru, Central Bank of Russia site: \
            <a>https://www.cbr.ru/currency_base/daily/</a>'
        bot.send_message(message.chat.id, text, parse_mode='html')


bot.polling(non_stop=True)