
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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
    welcome_text = (
        "Assalomu alaykum! Kushon Medical Servis botiga xush kelibsiz!
"
        "Zamonaviy laboratoriya tahlillari, aniq natijalar va professional xizmat sizni kutmoqda!

"
        "Quyidagi bo‘limlardan kerakli ma’lumotni tanlang:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = {
        "Tahlillar": "Bizda gormonlar, TORCH, onkomarkerlar, biokimyo va boshqa ko‘plab tahlillar mavjud.",
        "Biz bilan bog‘lanish": "Telefon: +998 90 741 72 22
Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida.",
        "Instagram manzil": "Instagram: https://instagram.com/akmal.jon7222",
        "Admin bilan bog‘lanish": "Admin: https://t.me/akmaljon_chatgpt_bot",
        "Tahlil natijalari": "Tahlil natijalari laboratoriyamiz orqali olinadi.",
        "Taklif va shikoyat": "Taklif va shikoyatlar uchun: +998 90 741 72 22",
        "Qon topshirishga tayyorgarlik": "Qon topshirishdan oldin 8-12 soat ovqat yemang, suv ichish mumkin.",
        "IXLA va IFA tekshuruv farqi": "IXLA – immunxemilyuminesens, aniq va tez usul.
IFA – fermentativ usul, kamroq sezgirlikda ishlaydi."
    }
    await update.message.reply_text(response.get(text, "Iltimos, menyudan tanlang."))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()
