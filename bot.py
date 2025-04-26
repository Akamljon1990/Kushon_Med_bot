from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

# Asosiy menyu
main_menu_keyboard = [
    ["Tahlillar haqida", "Qon topshirish qoidalari"],
    ["Bioximik tahlillar", "Klinik tahlillar"],
    ["IXLA va IFA farqi", "Biz bilan bog'lanish"],
    ["Tahlil natijalari", "Taklif va shikoyatlar"],
    ["Kitob (testlar haqida)", "Foydalanuvchi qo'shish"],
    ["Organizmda qanday o'zgarish?"],
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Kushon Medical Servis laboratoriyasi botiga xush kelibsiz!\n\nSiz biz bilan quyidagilarni amalga oshirishingiz mumkin:",
        reply_markup=main_menu
    )

# Tugma ishlovchi
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Tahlillar haqida":
        await update.message.reply_text("Tahlillar guruhlari: Gormonlar, TORCH, Onkomarkerlar, Vitaminlar va boshqalar...")
    elif text == "Qon topshirish qoidalari":
        await update.message.reply_text("Qon topshirishdan oldin 8-12 soat och qoling, ertalab soat 7:00-10:00 oralig'ida topshirish tavsiya etiladi.")
    elif text == "Bioximik tahlillar":
        await update.message.reply_text("Bioximik tahlillar ro'yxati: Glukoza, Kreatinin, AST, ALT, Bilirubin va boshqalar...")
    elif text == "Klinik tahlillar":
        await update.message.reply_text("Umumiy qon tahlili va umumiy siydik tahlili haqida ma'lumot.")
    elif text == "IXLA va IFA farqi":
        await update.message.reply_text("IXLA (Immunoximiolyuminestsent) tekshiruv zamonaviy va aniq. IFA esa eskiroq texnika hisoblanadi.")
    elif text == "Biz bilan bog'lanish":
        await update.message.reply_text("Biz bilan bog'lanish:\n📍 Kosonsoy tumani, Kattalar poliklinikasi yonida\n📞 +998 90 741 72 22\n📧 Akmaljon.19@bk.ru\n📷 Instagram: @akmal.jon7222\n💬 Telegram: @Akmaljon_lab")
    elif text == "Tahlil natijalari":
        await update.message.reply_text("ID raqamingizni yuboring, biz sizning tahlil natijalaringizni tekshirib beramiz.")
    elif text == "Taklif va shikoyatlar":
        await update.message.reply_text("Taklif va shikoyatlaringizni yozing, biz ularni adminga yetkazamiz.")
    elif text == "Kitob (testlar haqida)":
        await update.message.reply_text("📚 Testlar haqida to'liq ma'lumot (Kitob) pullik. Narxi: 45 000 so'm.\nAdmin bilan bog'lanish: @Akmaljon_lab")
    elif text == "Foydalanuvchi qo'shish":
        await update.message.reply_text("✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\nDo'stlaringizga ham botni ulashing: https://t.me/YOUR_BOT_USERNAME")
    elif text == "Organizmda qanday o'zgarish?":
        await update.message.reply_text("📋 Organizmingizdagi o'zgarish yoki shikoyatingizni yozing. Biz sizga qaysi tahlillar kerakligini tavsiya qilamiz.")
    else:
        await update.message.reply_text("Iltimos, menyudan kerakli bo'limni tanlang.")

# Callback funksiyasi (Inline tugmalar uchun kerak bo'lsa)
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Bu yerda inline tugmalar uchun alohida ishlovchi bo'lishi mumkin.")

# Main funksiyasi
def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
