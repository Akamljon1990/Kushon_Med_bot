import os
import telebot
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

# Tokenni olamiz
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Botni ishga tushuramiz
bot = telebot.TeleBot(BOT_TOKEN)

# /start buyrug'iga javob
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Kushon Medical Servis laboratoriya botiga xush kelibsiz!")

# Botni doimiy holatda ishlashga qo'yamiz
bot.infinity_polling()
