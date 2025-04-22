import telebot
import os

# Tokenni .env fayldan o'qish
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

# /start buyrug‘iga javob
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Kushon Medical Servis laboratoriyasi botiga xush kelibsiz!")

# Botni ishlatish
bot.infinity_polling()
