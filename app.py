import telebot
import requests
import json

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
    text = "Ask the bot to convert currency."
    bot.send_message(message.chat.id, text, parse_mode='html')
    
@bot.message_handler(content_types=['text'])
def handle_convert(message):
    """
    Check if we have the CBR data for the current day and download it
    if needed. Unpack it from JSON format.
    
    Дата не передаётся, при необходимости получить исторические данные запрос будет иметь вид:
    https://www.cbr-xml-daily.ru/archive/2020/06/02/daily_json.js
    
    Вместо USD пишем запрашиваемую валюту, кроме RUB, т.к. всё считается относительно рубля,
    и тут будем просто высчитывать в другую сторону.
    """
    
    cbr_data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    response = json.loads(cbr_data.content)
    currency = message.text
    bot.send_message(message.chat.id, response['Valute'][currency]['Value'])
    #with open('') as data_file:
    #    data = json.load(data_file)
    #print(data['Valute']['USD']['Value'])


bot.polling(none_stop=True)