
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tugmalar
main_menu = [['Test guruhlari'], ['Biz haqimizda', 'Admin bilan bogʻlanish'], ['Chiqish']]

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Kushon Medical Servis botiga xush kelibsiz!",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

app = ApplicationBuilder().token("TOKENINGIZNI_BU_YERGA_QO'YING").build()
app.add_handler(CommandHandler("start", start))

print("Bot ishga tushdi.")
app.run_polling()
