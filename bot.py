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
    ["Organizmda qanday o'zgarish?"]
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Gormonlar ro'yxati
hormone_buttons = [
    "TSH", "FT4", "FT3", "Prolaktin", "Estradiol", "Testosteron", "LH", "FSH", "Progesteron", "AMH",
    "Insulin", "C_peptid", "ACTH", "Kortizol", "PTH", "Vitamin_D", "HCG", "DHEA_S", "IGF_1", "Aldosteron",
    "Renin", "Androstenedion", "Adiponektin", "Ghrelin", "Leptin", "Beta-hCG", "Calcitonin", "Somatotropin",
    "Proinsulin", "SHBG", "17-OH Progesteron", "Anti-TPO", "Anti-Tg", "FSH/LH nisbati", "Insulin Resistence",
    "Melatonin", "Parathormon", "Free Estriol", "Inhibin B", "Mullerian Inhibiting Substance", "Oxytocin",
    "Relaxin", "Vasopressin", "Kisspeptin", "Adrenalin", "Noradrenalin", "Thyroglobulin", "Catecholamines",
    "Plazma Metanefrin"
]
hormone_keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in hormone_buttons]
hormone_menu = InlineKeyboardMarkup(hormone_keyboard)

# Har bir gormon haqida ma'lumot (Hozircha TSH va FT4, keyin barchasini to‘ldirib beraman)
hormone_info = {
    "TSH": "🔬 TSH (Qalqonsimon bez stimulyator gormoni)\n➔ Norma: 0.27 – 4.2 mIU/L\n📈 Oshganda: Gipotiroidizm\n📉 Kamayganda: Gipertiroidizm\n⚡ Belgilar: Holsizlik, sovuqqa sezuvchanlik, vazn ortishi.\n🕒 Tekshirish: Holsizlik va qalqonsimon bez kasalliklari belgilari.",
    "FT4": "🔬 FT4 (Erkin Tiroksin)\n➔ Norma: 0.93 – 1.7 ng/dL\n📈 Oshganda: Gipertiroidizm\n📉 Kamayganda: Gipotiroidizm\n⚡ Belgilar: Yurak urishining tezlashishi, vazn kamayishi.\n🕒 Tekshirish: Qalqonsimon bez faoliyati shubhasida."
}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Kushon Medical Servis laboratoriyasi botiga xush kelibsiz!\n\nMenyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )

# Menyudagi tugmalarni ishlovchi
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Tahlillar haqida":
        await update.message.reply_text("Gormonlar ro'yxati:", reply_markup=hormone_menu)
    elif text == "Qon topshirish qoidalari":
        await update.message.reply_text("Qon topshirishdan oldin 8-12 soat och qolish tavsiya etiladi. Ertalab soat 7-10 oralig'ida.")
    elif text == "Bioximik tahlillar":
        await update.message.reply_text("Bioximik tahlillar: Glukoza, Kreatinin, AST, ALT, Bilirubin va boshqalar.")
    elif text == "Klinik tahlillar":
        await update.message.reply_text("Klinik tahlillar: Umumiy qon tahlili va siydik tahlili haqida.")
    elif text == "IXLA va IFA farqi":
        await update.message.reply_text("IXLA zamonaviy va aniq, IFA esa nisbatan eski texnologiya.")
    elif text == "Biz bilan bog'lanish":
        await update.message.reply_text("Manzil: Kosonsoy tumani, Poliklinika yonida.\nTelefon: +998907417222\nInstagram: @akmal.jon7222\nTelegram: @Akmaljon_lab\nEmail: Akmaljon.19@bk.ru")
    elif text == "Tahlil natijalari":
        await update.message.reply_text("ID raqamingizni yuboring.")
    elif text == "Taklif va shikoyatlar":
        await update.message.reply_text("Taklif va shikoyatlaringizni yozib yuboring.")
    elif text == "Kitob (testlar haqida)":
        await update.message.reply_text("📚 Testlar haqida kitob pullik! Narxi: 45 000 so'm.\nAdmin bilan bog'laning: @Akmaljon_lab")
    elif text == "Foydalanuvchi qo'shish":
        await update.message.reply_text("✅ Ro'yxatdan o'tdingiz! Botni do'stlaringizga tavsiya qiling.")
    elif text == "Organizmda qanday o'zgarish?":
        await update.message.reply_text("📋 Organizmingizdagi o'zgarish yoki shikoyatni yozing, biz sizga mos tahlillarni tavsiya qilamiz.")
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.")

# Inline tugmalar ishlovchi
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    info = hormone_info.get(query.data)
    if info:
        await query.edit_message_text(info)
    else:
        await query.edit_message_text("Bu test haqida ma'lumot hali tayyor emas.")

# Main funksiyasi
def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Bot token topilmadi. Iltimos, .env faylga TOKEN kiriting.")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Bot ishga tushdi...")
    app.run_polling()
# Har bir gormon haqida to'liq ma'lumot
hormone_info = {
    "TSH": "🔬 TSH (Qalqonsimon bez stimulyator gormoni)\n"
           "➔ Norma: 0.27 – 4.2 mIU/L\n\n"
           "📈 Oshganda:\n"
           "- Gipotiroidizm (qalqonsimon bez faoliyatining pasayishi)\n"
           "- Hashimoto tireoiditi (autoimmun kasallik)\n"
           "- Qalqonsimon bezni jarrohlik yoki radiatsiya bilan olib tashlash\n\n"
           "📉 Kamayganda:\n"
           "- Gipertiroidizm (qalqonsimon bez faoliyatining ortishi)\n"
           "- Graves kasalligi (autoimmun gipertiroidizm)\n"
           "- Nodular toksik zob\n\n"
           "⚡ Organizmdagi belgilar:\n"
           "- Holsizlik va tez charchash\n"
           "- Sovuqqa sezuvchanlik\n"
           "- Vazn ortishi yoki kamayishi\n"
           "- Ruhiy tushkunlik\n"
           "- Yurak urishining buzilishi (sekin yoki tez)\n"
           "- Tana haroratining pasayishi yoki ko‘tarilishi\n"
           "- Teri qurishi va soch to‘kilishi\n\n"
           "⏰ Qachon tekshirish kerak:\n"
           "- Charchoq va kuchsizlik\n"
           "- Qorinning shishishi yoki vazn ortishi\n"
           "- Sovuqqa sezuvchanlik kuchayganda\n"
           "- Hayz siklining buzilishi\n"
           "- Homiladorlikda qalqonsimon bezni nazorat qilishda"
}
