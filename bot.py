import os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("Salom! Kushon Medical Servis botiga xush kelibsiz.")

updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
