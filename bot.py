from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os
# Asosiy menyu (start uchun)
main_menu = ReplyKeyboardMarkup([
    ["🧪 Tahlillar", "📄 Tahlil natijalari"],
    ["📞 Biz bilan bog‘lanish", "👨‍💼 Admin bilan muloqot"],
    ["📷 Instagram sahifamiz", "💬 Taklif va shikoyat"],
    ["🩸 Qon topshirishga tayyorgarlik", "🧬 IXLA va IFA farqi"]
], resize_keyboard=True)
# Asosiy menyu (start uchun)
main_menu = ReplyKeyboardMarkup([
    ["🧪 Tahlillar", "📄 Tahlil natijalari"],
    ["📞 Biz bilan bog‘lanish", "👨‍💼 Admin bilan muloqot"],
    ["📷 Instagram sahifamiz", "💬 Taklif va shikoyat"],
    ["🩸 Qon topshirishga tayyorgarlik", "🧬 IXLA va IFA farqi"]
], resize_keyboard=True)

# Tahlillar menyusi (test guruhlari uchun)
tahlillar_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("1. Gormonlar", callback_data='gormonlar')],
    [InlineKeyboardButton("2. TORCH paneli", callback_data='torch')],
    [InlineKeyboardButton("3. Onkomarkerlar", callback_data='onkomarker')],
    [InlineKeyboardButton("4. Vitaminlar va Anemiya", callback_data='vitamin')],
    [InlineKeyboardButton("5. Kardiomarkerlar", callback_data='kardio')],
    [InlineKeyboardButton("6. Koagulyatsiya", callback_data='koagul')],
    [InlineKeyboardButton("7. Suyak metabolizmi", callback_data='suyak')],
    [InlineKeyboardButton("8. Jigar fibrozi", callback_data='jigar')],
    [InlineKeyboardButton("9. Buyrak funksiyasi", callback_data='buyrak')],
    [InlineKeyboardButton("10. Immunoglobulinlar", callback_data='immun')],
    [InlineKeyboardButton("11. Autoimmun panel", callback_data='autoimmun')],
    [InlineKeyboardButton("12. Yuqumli kasalliklar", callback_data='infeksiya')],
    [InlineKeyboardButton("13. Allergenlar", callback_data='allergen')],
    [InlineKeyboardButton("14. Dori nazorati", callback_data='dori')]
])
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\nKushon Medical Servis laboratoriyasi rasmiy botiga xush kelibsiz.\nPastdagi menyudan kerakli bo‘limni tanlang 👇",
        reply_markup=main_menu
    )
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🧪 Tahlillar":
        await update.message.reply_text(
            "Quyidagi test guruhlaridan birini tanlang:", reply_markup=tahlillar_menu
        )
    else:
        await update.message.reply_text("Iltimos, menyudan biror bo‘limni tanlang.")
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "gormonlar":
        await query.edit_message_text("🧪 Gormonlar haqida batafsil ma’lumot...")
    elif query.data == "torch":
        await query.edit_message_text("🧪 TORCH paneli haqida batafsil ma’lumot...")
    # va hokazo barcha testlar uchun shunday yozib chiqamiz.
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
