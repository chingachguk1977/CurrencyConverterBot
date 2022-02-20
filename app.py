import telebot
#TODO база данный по субтитрам

TOKEN = "5156928592:AAHs5egCtuMoEZl7xxyg3yRI0iQtSU4XfQo"

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    bot.reply_to(message, "У тебя красивый голос!")

# Обрабатываются все голосовые сообщения.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Да чё ты доебался? Ничего я не умею!")

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, "Твои файлики попадут куда надо!")

# Обрабатывается все текстовые сообщения
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, f"Привет, {message.chat.username}!")

# Обрабатывается все картинки
@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, "Nice meme XDD")


bot.polling(none_stop=True)