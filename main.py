from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from Menu import get_main_menu

# START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Kushon Medical botiga xush kelibsiz.\n\nIltimos, menyudan tanlang.",
        reply_markup=get_main_menu()
    )

# Reklama/Spam filtri
async def filter_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(keyword in text for keyword in ["@", "http", "t.me", "vpn", "jeton"]):
        await update.message.delete()
        await update.message.reply_text("❌ Reklama yoki havolalar yuborish taqiqlangan.")
    else:
        await handle_menu_selection(update, context)

# Menyu ishlovchi
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "Tahlillar haqida ma'lumot":
        await update.message.reply_text("Bu yerda tahlillar haqida umumiy ma’lumotlar keltiriladi...")
    elif user_text == "Qon topshirish qoidalari":
        await update.message.reply_text("Qon topshirishdan oldin 8–12 soat och bo‘lish kerak...")
    elif user_text == "Bioximiya haqida":
        await update.message.reply_text("Bioximiya tahlillari organizmdagi moddalar almashinuvini ko‘rsatadi...")
    elif user_text == "Klinika haqida":
        await update.message.reply_text("Bizning klinika Kosonsoy tumanida joylashgan...")
    elif user_text == "IXLA va IFA tekshiruv farqi":
        await update.message.reply_text("IXLA – zamonaviy immunokimyoviy usul, IFA esa fermentli usul...")
    elif user_text == "Biz bilan bog'lanish":
        await update.message.reply_text("Tel: +998 90 741 72 22\nInstagram: @akmal.jon7222\nTelegram: t.me/+998907417222")
    elif user_text == "Admin bilan bog'lanish":
        await update.message.reply_text("Admin: @akmaljon_admin")
    else:
        await update.message.reply_text("Iltimos, menyudan biror tugmani tanlang.")

# Asosiy ishga tushirish
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("❗ TOKEN topilmadi. .env faylga TOKEN=... ni yozing.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_spam))
    app.run_polling()
