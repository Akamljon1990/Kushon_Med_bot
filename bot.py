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
"FT4": "🔬 FT4 (Erkin Tiroksin)\n➔ Norma: 0.93 – 1.7 ng/dL\n📈 Oshganda: Gipertiroidizm\n📉 Kamayganda: Gipotiroidizm\n⚡ Belgilar: Yurak urishining tezlashishi, vazn kamayishi.\n🕒 Tekshirish: Qalqonsimon bez faoliyati shubhasida.",
"FT3": "🔬 FT3 (Erkin Triiyodtironin)\n➔ Norma: 2.0 – 4.4 pg/mL\n📈 Oshganda: Gipertiroidizm\n📉 Kamayganda: Gipotiroidizm\n⚡ Belgilar: Tez yurak urishi, ishtaha o‘zgarishi.\n🕒 Tekshirish: Qalqonsimon bez buzilishi belgilari mavjud bo‘lsa.",
"Prolaktin": "🔬 Prolaktin\n➔ Norma: Ayollar: 4.8 – 23.3 ng/mL, Erkaklar: 4.0 – 15.2 ng/mL\n📈 Oshganda: Giperprolaktinemiya\n📉 Kamayganda: Gormon yetishmovchiligi\n⚡ Belgilar: Beqaror hayz, bepushtlik, ko‘krakdan suyuqlik ajralishi.\n🕒 Tekshirish: Hayz buzilishi, bepushtlikda.",
"Estradiol": "🔬 Estradiol\n➔ Norma: Ayollar (folikulyar faza): 12.5-166 pg/mL\n📈 Oshganda: Ovarian kistalar\n📉 Kamayganda: Menopauza\n⚡ Belgilar: Hayz davri buzilishi, ko‘ngil aynish.\n🕒 Tekshirish: Homiladorlik yoki hayz siklining buzilishi shubhasida.",
"Testosteron": "🔬 Testosteron\n➔ Norma: Erkaklar: 300–1000 ng/dL, Ayollar: 15–70 ng/dL\n📈 Oshganda: Polikistoz tuxumdon\n📉 Kamayganda: Hipogonadizm\n⚡ Belgilar: Soch to‘kilishi, libidoning pasayishi.\n🕒 Tekshirish: Libido pasayishi yoki jinsiy disfunktsiyada.",
"LH": "🔬 LH (Luteinizing gormon)\n➔ Norma: Erkaklar: 1.24–7.8 IU/L, Ayollar: 1.68–15 IU/L\n📈 Oshganda: Ovulyatsiya\n📉 Kamayganda: Gormon yetishmovchiligi\n⚡ Belgilar: Bezararlik, hayz buzilishi.\n🕒 Tekshirish: Gormon yetishmovchiligi va bepushtlik tekshiruvlarida.",
"FSH": "🔬 FSH (Follikula stimulyator gormoni)\n➔ Norma: Erkaklar: 1.5–12.4 IU/L, Ayollar: 3.5–12.5 IU/L\n📈 Oshganda: Menopauza\n📉 Kamayganda: Gormon yetishmovchiligi\n⚡ Belgilar: Hayz buzilishi, bepushtlik.\n🕒 Tekshirish: Hayz siklining buzilishi va bepushtlik shubhasida.",
"Progesteron": "🔬 Progesteron\n➔ Norma: Luteal faza: 5–20 ng/mL\n📈 Oshganda: Homiladorlik\n📉 Kamayganda: Homiladorlik xavfi\n⚡ Belgilar: Hayz buzilishi, homiladorlikda xavf.\n🕒 Tekshirish: Homiladorlik nazorati va luteal fazani tekshirishda.",
"AMH": "🔬 AMH (Anti-Mullerian Gormon)\n➔ Norma: 1–10 ng/mL\n📈 Oshganda: Polikistoz tuxumdon sindromi\n📉 Kamayganda: Ovarian rezerva kamayishi\n⚡ Belgilar: Beqaror hayz sikli.\n🕒 Tekshirish: Tuxumdon zaxirasini baholash uchun.",
"Insulin": "🔬 Insulin\n➔ Norma: 2.6–24.9 μIU/mL\n📈 Oshganda: Insulin rezistentlik\n📉 Kamayganda: Diabetes mellitus\n⚡ Belgilar: Vazn ortishi, charchoq.\n🕒 Tekshirish: Qandli diabet shubhasida.",
"C_peptid": "🔬 C-peptid\n➔ Norma: 0.5–2.0 ng/mL\n📈 Oshganda: Insulinoma\n📉 Kamayganda: Diabetes mellitus\n⚡ Belgilar: Glyukoza darajasining buzilishi.\n🕒 Tekshirish: Insulin sekretsiyasini baholashda.",
"ACTH": "🔬 ACTH (Adrenokortikotropik gormon)\n➔ Norma: 10–60 pg/mL\n📈 Oshganda: Kuşing kasalligi\n📉 Kamayganda: Addison kasalligi\n⚡ Belgilar: Qon bosimi o‘zgarishi, teri rangi o‘zgarishi.\n🕒 Tekshirish: Adrenal bez faoliyatini tekshirishda.",
"Kortizol": "🔬 Kortizol\n➔ Norma: 6–23 mcg/dL\n📈 Oshganda: Kuşing sindromi\n📉 Kamayganda: Addison kasalligi\n⚡ Belgilar: Qon bosimi, stressga javob reaksiyasi.\n🕒 Tekshirish: Stress va adrenal kasallik shubhasida.",
"PTH": "🔬 PTH (Paratireoid gormon)\n➔ Norma: 10–65 pg/mL\n📈 Oshganda: Giperparatireoz\n📉 Kamayganda: Gipoparatireoz\n⚡ Belgilar: Qon kaltsiy darajasi o‘zgarishi.\n🕒 Tekshirish: Kaltsiy metabolizmi buzilishlarida.",
"Vitamin_D": "🔬 Vitamin D\n➔ Norma: 30–100 ng/mL\n📈 Oshganda: Intoksikatsiya\n📉 Kamayganda: Raxit, osteoporoz\n⚡ Belgilar: Suyak zaifligi, charchoq.\n🕒 Tekshirish: D vitamini yetishmovchiligi shubhasida.",
"HCG": "🔬 HCG (Homiladorlik gormoni)\n➔ Norma: Homilador bo‘lmaganlarda: <5 mIU/mL\n📈 Oshganda: Homiladorlik\n📉 Kamayganda: Homiladorlikda xavf\n⚡ Belgilar: Homiladorlik belgilari.\n🕒 Tekshirish: Homiladorlikni tasdiqlash uchun.",
"DHEA_S": "🔬 DHEA-S\n➔ Norma: 80–560 mcg/dL\n📈 Oshganda: Virilizatsiya\n📉 Kamayganda: Adrenal yetishmovchilik\n⚡ Belgilar: Tana sochlari o‘sishi.\n🕒 Tekshirish: Androgen sekretsiyasini baholashda.",
"IGF_1": "🔬 IGF-1\n➔ Norma: Yoshga qarab o‘zgaradi\n📈 Oshganda: Gigantizm\n📉 Kamayganda: O‘sish gormon yetishmovchiligi\n⚡ Belgilar: O‘sish buzilishi.\n🕒 Tekshirish: O‘sish gormonini baholashda.",
"Aldosteron": "🔬 Aldosteron\n➔ Norma: 4–31 ng/dL\n📈 Oshganda: Giperaldosteronizm\n📉 Kamayganda: Giporeninemik giporeninemiya\n⚡ Belgilar: Qon bosimi o‘zgarishi.\n🕒 Tekshirish: Qon bosimi nazoratida.",
"Renin": "🔬 Renin\n➔ Norma: 0.5–4.0 ng/mL/h\n📈 Oshganda: Gipertoniya\n📉 Kamayganda: Addison kasalligi\n⚡ Belgilar: Qon bosimining o‘zgarishi.\n🕒 Tekshirish: Renin-aldosteron tizimini baholashda.",
"Androstenedion": "🔬 Androstenedion\n➔ Norma: 0.7–3.1 ng/mL\n📈 Oshganda: Virilizatsiya\n📉 Kamayganda: Gormon yetishmovchiligi\n⚡ Belgilar: Akne, soch o‘sishining ko‘payishi.\n🕒 Tekshirish: Androgen buzilishlarida.",
"Adiponektin": "🔬 Adiponektin\n➔ Norma: 4–26 mcg/mL\n📈 Oshganda: Anoreksiya\n📉 Kamayganda: Obezlik, diabet\n⚡ Belgilar: Metabolik sindrom.\n🕒 Tekshirish: Semizlik va metabolik kasalliklarda."
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

    if __name__ == "__main__":
        main()


