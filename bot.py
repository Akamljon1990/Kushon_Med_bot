
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Tahlillar", callback_data='tahlillar')],
        [InlineKeyboardButton("Biz haqimizda", callback_data='biz')],
        [InlineKeyboardButton("Admin bilan muloqot", callback_data='admin')],
        [InlineKeyboardButton("Instagram", callback_data='instagram')],
        [InlineKeyboardButton("Narxlar", callback_data='narx')],
        [InlineKeyboardButton("Tahlil natijalari", callback_data='natija')],
    ]
    await update.message.reply_text("Kerakli bo‘limni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    javoblar = {
        "tahlillar": "Test guruhlari: Gormonlar, TORCH, Onkomarkerlar, Kardiomarkerlar, Biokimyo, Umumiy qon, Siydik, Vitaminlar va boshqalar.",
        "biz": "Kushon Medical Servis – zamonaviy laboratoriya. Kosonsoy tumani, Kattalar poliklinikasi yonida.",
        "admin": "Admin bilan bog‘lanish: @akmaljon_chatgpt_bot",
        "instagram": "Instagram: https://instagram.com/akmal.jon7222",
        "narx": "Narxlar haqida ma’lumot laboratoriya qabulida beriladi.",
        "natija": "Tahlil natijalari uchun laboratoriya qabuliga murojaat qiling."
    }
    await query.edit_message_text(javoblar.get(data, "Bo‘lim topilmadi."))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
