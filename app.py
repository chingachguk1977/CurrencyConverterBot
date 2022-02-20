import telebot
#TODO база данный по субтитрам

TOKEN = "5156928592:AAHs5egCtuMoEZl7xxyg3yRI0iQtSU4XfQo"

bot = telebot.TeleBot(TOKEN)

currecies = {
    'Dollar': 'USD',
    'Ruble': 'RUB',
    'Euro': 'EUR'
}

@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    bot.reply_to(message, "У тебя красивый голос!")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message) -> None:
    """
    The method handles two commands: '/start' and '/help' and gives the invitation.
    """
    text = "Ask the bot to convert currency."
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)