import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["Tahlillar", "Biz bilan bog‘lanish"],
        ["Instagram manzil", "Admin bilan bog‘lanish"],
        ["Tahlil natijalari", "Taklif va shikoyat"],
        ["Qon topshirishga tayyorgarlik", "IXLA va IFA tekshuruv farqi"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """Assalomu alaykum! Kushon Medical Servis botiga xush kelibsiz!

Zamonaviy laboratoriya tahlillari endi sizga yaqin!

Quyidagi bo‘limlardan keraklisini tanlang:"""
    await update.message.reply_text(welcome_text, reply_markup=main_menu)

if __name__ == "__main__":
    from telegram.ext import MessageHandler, filters
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
