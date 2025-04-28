from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

# Asosiy menyu
main_menu_keyboard = [
    ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"],
    ["Bioximiya haqida", "Klinika haqida"],
    ["IXLA va IFA tekshiruv farqi"],
    ["Biz bilan bog'lanish", "Admin bilan bog'lanish"],
    ["Tahlil natijalarini olish", "Taklif va shikoyatlar"],
    ["Kitob (Analizlar haqida to‘liq ma'lumot)"],
    ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilmoqda?"]
]

main_menu = ReplyKeyboardMarkup(
    keyboard=main_menu_keyboard,
    resize_keyboard=True
)

# Gormonlar ro'yxati
hormone_buttons = [
    "TSH", "FT4", "FT3", "Prolaktin", "Estradiol", "Testosteron", "LH", "FSH", "Progesteron", "AMH",
    "Insulin", "C_peptid", "ACTH", "Kortizol", "PTH", "Vitamin_D", "HCG", "DHEA_S", "IGF_1", "Aldosteron",
    "Renin", "Androstenedion", "Adiponektin", "Ghrelin", "Leptin", "Beta-hCG", "Calcitonin", "Somatotropin",
    "Proinsulin", "SHBG", "17-OH Progesteron", "Anti-TPO", "Anti-Tg", "Insulin Resistence",
    "Melatonin", "Parathormon", "Free Estriol", "Inhibin B", "Mullerian Inhibiting Substance", "Oxytocin",
    "Relaxin", "Vasopressin", "Kisspeptin", "Adrenalin", "Noradrenalin", "Thyroglobulin", "Catecholamines",
    "Plazma Metanefrin"
]
hormone_keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in hormone_buttons]
hormone_menu = InlineKeyboardMarkup(hormone_keyboard)

# Gormonlar haqida ma'lumotlar
hormone_info = {
    "TSH": "🔬 TSH haqida ma'lumot...",
    "FT4": "🔬 FT4 haqida ma'lumot...",
    # (Qolgan gormonlar uchun ham xuddi shunday ma'lumotlar bo'lishi kerak)
}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧬 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n"
        "🔬 Biz zamonaviy IXLA texnologiyasi asosida:\n"
        "– Gormonlar\n"
        "– TORCH Paneli\n"
        "– Onkomarkerlar\n"
        "– Bioximik tahlillar\n"
        "– Umumiy qon va siydik tahlillarini sifatli va tezkor amalga oshiramiz.\n\n"
        "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n"
        "📞 Telefon: +998 90 741 72 22\n"
        "📸 Instagram: @akmal.jon7222\n\n"
        "✅ Biz uchun daromaddan ko‘ra **to‘g‘ri natija va bemor ishonchi muhim**!\n\n"
        "✅ Ishonchli diagnostika – sog‘ligingiz kafolati!",
        reply_markup=main_menu
    )

# Inline tugmalar uchun callback
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    info = hormone_info.get(query.data)
    if info:
        await query.edit_message_text(info)
    else:
        await query.edit_message_text("Bu test haqida ma'lumot hali tayyor emas.")

# Menyu tugmalarini boshqarish
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Tahlillar haqida ma'lumot":
        await update.message.reply_text("Gormonlar, TORCH paneli, Onkomarkerlar va boshqalar haqida tanlang.", reply_markup=hormone_menu)
    elif text == "Qon topshirish qoidalari":
        await update.message.reply_text("Qon topshirish uchun:\n- 8-12 soat och qoling.\n- Ertalab soat 7:00-10:00 oralig'ida topshirish tavsiya etiladi.\n- Suv ichish mumkin.")
    elif text == "Bioximiya haqida":
        await update.message.reply_text("Bioximiya tahlillariga: jigar, buyrak, yurak, suyak va boshqa organlarning ko'rsatkichlari kiradi.")
    elif text == "Klinika haqida":
        await update.message.reply_text("Klinik tahlillar umumiy qon analizi, siydik analizi va boshqa testlarni o'z ichiga oladi.")
    elif text == "IXLA va IFA tekshiruv farqi":
        await update.message.reply_text("IXLA - zamonaviy, tezkor va aniq tekshiruv. IFA esa eskirganroq usul. IXLA ko'proq ishonch beradi.")
    elif text == "Biz bilan bog'lanish":
        await update.message.reply_text("Biz bilan bog'lanish:\n📍 Kosonsoy tumani, Kattalar poliklinikasi yonida\n📞 +998 90 741 72 22\n📸 Instagram: @akmal.jon7222\n✉️ Email: akmaljon.1990k.ru@gmail.com")
    elif text == "Admin bilan bog'lanish":
        await update.message.reply_text("Admin bilan bog'lanish uchun @akmaljon_lab ga yozing.")
    elif text == "Tahlil natijalarini olish":
        await update.message.reply_text("Tahlil natijasini olish uchun ID raqamingizni kiriting:")
    elif text == "Taklif va shikoyatlar":
        await update.message.reply_text("Taklif yoki shikoyatingizni yozing. Xabaringiz adminga yuboriladi.")
    elif text == "Kitob (Analizlar haqida to‘liq ma'lumot)":
        await update.message.reply_text("Testlar haqida to‘liq ma’lumot olish uchun ‘Kitob’ so‘zini adminga yuboring.\nNarxi: 45 000 so‘m. ❗️ Pullik xizmat!")
    elif text == "Botga foydalanuvchi qo‘shish":
        await update.message.reply_text("Bot foydali bo‘lsa, do‘stlaringizga ham tavsiya qiling!")
    elif text == "Sizni nima bezovta qilmoqda?":
        await update.message.reply_text("Bizga yozing! Biz maslahat berishga tayyormiz.")
    else:
        await update.message.reply_text("Iltimos, menyudan tugmani tanlang.")

# Main funksiyasi
def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Bot token topilmadi. Iltimos, .env faylga TOKEN kiriting.")
    
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

# Dastur ishga tushuruvchi qism
if __name__ == "__main__":
    main()
