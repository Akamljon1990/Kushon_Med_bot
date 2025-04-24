import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Assalomu alaykum! Kushon Medical Servis laboratoriyasining rasmiy botiga xush kelibsiz.')

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
