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

# Har bir gormon haqida qisqacha ma'lumot
hormone_info = {
    "TSH": "🔬 TSH (Qalqonsimon bez stimulyator gormoni)\n➔ Norma: 0.27–4.2 mIU/L\n📈 Oshganda: Gipotiroidizm\n📉 Kamayganda: Gipertiroidizm\n⚡ Belgilar: Holsizlik, sovuqqa sezuvchanlik, vazn ortishi.\n🕒 Tekshirish: Qalqonsimon bez faoliyati uchun.",
    "FT4": "🔬 FT4 (Erkin Tiroksin)\n➔ Norma: 0.93–1.7 ng/dL\n📈 Oshganda: Gipertiroidizm\n📉 Kamayganda: Gipotiroidizm\n⚡ Belgilar: Yurak urishi, vazn kamayishi.",
    "FT3": "🔬 FT3 (Erkin Triiyodtironin)\n➔ Norma: 2.0–4.4 pg/mL\n📈 Oshganda: Gipertiroidizm\n📉 Kamayganda: Gipotiroidizm\n⚡ Belgilar: Yurak urishi, ishtaha o‘zgarishi.",
    "Prolaktin": "🔬 Prolaktin\n➔ Norma: Ayollar 4.8–23.3 ng/mL, Erkaklar 4.0–15.2 ng/mL\n📈 Oshganda: Giperprolaktinemiya\n⚡ Belgilar: Hayz buzilishi, ko‘krakdan suyuqlik.",
    "Estradiol": "🔬 Estradiol\n➔ Norma: 12.5–166 pg/mL (folikulyar faza)\n📈 Oshganda: Ovarian kista\n📉 Kamayganda: Menopauza\n⚡ Belgilar: Hayz buzilishi.",
    "Testosteron": "🔬 Testosteron\n➔ Norma: Erkaklar 300–1000 ng/dL, Ayollar 15–70 ng/dL\n📈 Oshganda: Polikistoz tuxumdon\n📉 Kamayganda: Hipogonadizm\n⚡ Belgilar: Libidoning pasayishi.",
    "LH": "🔬 LH (Luteinizing gormon)\n➔ Norma: 1.24–7.8 IU/L\n📈 Oshganda: Ovulyatsiya\n📉 Kamayganda: Gormon yetishmovchiligi.",
    "FSH": "🔬 FSH (Follikula stimulyator gormoni)\n➔ Norma: 3.5–12.5 IU/L\n📈 Oshganda: Menopauza\n📉 Kamayganda: Hayz buzilishi.",
    "Progesteron": "🔬 Progesteron\n➔ Norma: 5–20 ng/mL (luteal faza)\n📈 Oshganda: Homiladorlik\n📉 Kamayganda: Xavfli homiladorlik.",
    "AMH": "🔬 AMH (Anti-Mullerian Gormon)\n➔ Norma: 1–10 ng/mL\n📈 Oshganda: Polikistoz tuxumdon\n📉 Kamayganda: Tuxumdon zaxirasining kamayishi.",
    "Insulin": "🔬 Insulin\n➔ Norma: 2.6–24.9 μIU/mL\n📈 Oshganda: Insulin rezistentlik\n📉 Kamayganda: Qandli diabet.",
    "C_peptid": "🔬 C-peptid\n➔ Norma: 0.5–2.0 ng/mL\n📈 Oshganda: Insulinoma\n📉 Kamayganda: Insulin yetishmovchiligi.",
    "ACTH": "🔬 ACTH (Adrenokortikotropik gormon)\n➔ Norma: 10–60 pg/mL\n📈 Oshganda: Kuşing kasalligi\n📉 Kamayganda: Addison kasalligi.",
    "Kortizol": "🔬 Kortizol\n➔ Norma: 6–23 mcg/dL\n📈 Oshganda: Stressga javob reaksiyasi\n📉 Kamayganda: Addison kasalligi.",
    "PTH": "🔬 PTH (Paratireoid gormon)\n➔ Norma: 10–65 pg/mL\n📈 Oshganda: Giperparatireoz\n📉 Kamayganda: Gipoparatireoz.",
    "Vitamin_D": "🔬 Vitamin D\n➔ Norma: 30–100 ng/mL\n📉 Kamayganda: Raxit, suyak zaifligi.",
    "HCG": "🔬 HCG (Homiladorlik gormoni)\n➔ Norma: <5 mIU/mL (homilador bo‘lmagan)\n📈 Oshganda: Homiladorlik.",
    "DHEA_S": "🔬 DHEA-S\n➔ Norma: 80–560 mcg/dL\n📈 Oshganda: Androgen ko‘payishi.",
    "IGF_1": "🔬 IGF-1\n➔ Norma: Yoshga qarab o‘zgaradi\n📈 Oshganda: Gigantizm\n📉 Kamayganda: O‘sish sekinlashishi.",
    "Aldosteron": "🔬 Aldosteron\n➔ Norma: 4–31 ng/dL\n📈 Oshganda: Gipertoniya.",
    "Renin": "🔬 Renin\n➔ Norma: 0.5–4.0 ng/mL/h\n📈 Oshganda: Gipertoniya\n📉 Kamayganda: Addison kasalligi.",
    "Androstenedion": "🔬 Androstenedion\n➔ Norma: 0.7–3.1 ng/mL\n📈 Oshganda: Virilizatsiya (erkaklashish).",
    "Adiponektin": "🔬 Adiponektin\n➔ Norma: 4–26 mcg/mL\n📉 Kamayganda: Semizlik, diabet xavfi.",
    "Ghrelin": "🔬 Ghrelin\n➔ Norma: Individuallik farqlanadi\n📈 Oshganda: Ochlik hissi oshadi.",
    "Leptin": "🔬 Leptin\n➔ Norma: Farq qiladi (tana yog'iga bog'liq)\n📈 Oshganda: Semizlik bilan bog'liq muammolar.",
    "Beta-hCG": "🔬 Beta-hCG\n➔ Homiladorlik testida aniqlanadi.\n📈 Oshganda: Homiladorlik belgisi.",
    "Calcitonin": "🔬 Kalsitonin\n➔ Qalqonsimon bez bilan bog‘liq o‘zgarishlar indikatoridir.",
    "Somatotropin": "🔬 O‘sish gormoni (Somatotropin)\n📈 Oshganda: Gigantizm\n📉 Kamayganda: O‘sish sekinlashadi.",
    "Proinsulin": "🔬 Proinsulin\n➔ Norma: <20% umumiy insulin ichida.",
    "SHBG": "🔬 SHBG (Jinsiy gormon bilan bog'lovchi globulin)\n➔ Gormonlarning faolligini nazorat qiladi.",
    "17-OH Progesteron": "🔬 17-OH Progesteron\n➔ Norma: 0.2–1.3 ng/mL\n📈 Oshganda: Tug'ma adrenal giperplaziya.",
    "Anti-TPO": "🔬 Anti-TPO\n➔ Autoimmun tireoidit belgisi.",
    "Anti-Tg": "🔬 Anti-Tg\n➔ Tireoglobulinga qarshi antitelolar, autoimmun kasalliklar indikatoridir.",
    "Insulin Resistence": "🔬 Insulin rezistentlik\n➔ Qandli diabet xavfi oshadi.",
    "Melatonin": "🔬 Melatonin\n➔ Uyqu va biologik ritmni tartibga soladi.",
    "Parathormon": "🔬 Parathormon\n➔ Qon kaltsiy muvozanatini boshqaradi.",
    "Free Estriol": "🔬 Erkin estriol\n➔ Homiladorlik vaqtida baholanadi.",
    "Inhibin B": "🔬 Inhibin B\n➔ Tuxumdon va urug‘don funksiyasini baholaydi.",
    "Mullerian Inhibiting Substance": "🔬 Mullerian Inhibiting Substance\n➔ Reproduktiv tizim rivojlanishini ko‘rsatadi.",
    "Oxytocin": "🔬 Oksitotsin\n➔ Tug‘ruq va sut ajratish jarayonida rol o‘ynaydi.",
    "Relaxin": "🔬 Relaxin\n➔ Tug‘ruqqa tayyorlovchi gormon.",
    "Vasopressin": "🔬 Vazopressin\n➔ Qon bosimini va suv balansini nazorat qiladi.",
    "Kisspeptin": "🔬 Kisspeptin\n➔ Jinsiy yetilish boshlanishida ishtirok etadi.",
    "Adrenalin": "🔬 Adrenalin\n➔ Stress reaksiyalarini kuchaytiradi.",
    "Noradrenalin": "🔬 Noradrenalin\n➔ Stressga javob va qon bosimini tartibga soladi.",
    "Thyroglobulin": "🔬 Tireoglobulin\n➔ Qalqonsimon bez kasalliklarining markeridir.",
    "Catecholamines": "🔬 Katexolaminlar\n➔ Stress va adrenalin reaksiyalari indikatorlari.",
    "Plazma Metanefrin": "🔬 Plazma metanefrinlar\n➔ Feoxromositoma diagnostikasida muhim marker."
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
        await update.message.reply_text("Qon topshirishdan oldin 8-12 soat och qolish tavsiya etiladi. Ertalab 7-10 oralig'ida.")
    elif text == "Bioximik tahlillar":
        await update.message.reply_text("Bioximik tahlillar: Glukoza, Kreatinin, AST, ALT, Bilirubin va boshqalar.")
    elif text == "Klinik tahlillar":
        await update.message.reply_text("Klinik tahlillar: Umumiy qon va siydik tahlili haqida.")
    elif text == "IXLA va IFA farqi":
        await update.message.reply_text("IXLA zamonaviy va aniq metod, IFA esa eskiroq texnologiya.")
    elif text == "Biz bilan bog'lanish":
        await update.message.reply_text(
            "Manzil: Kosonsoy tumani, Poliklinika yonida.\n"
            "Telefon: +998907417222\n"
            "Instagram: @akmal.jon7222\n"
            "Telegram: @Akmaljon_lab\n"
            "Email: Akmaljon.19@bk.ru"
        )
    elif text == "Tahlil natijalari":
        await update.message.reply_text("ID raqamingizni yuboring.")
    elif text == "Taklif va shikoyatlar":
        await update.message.reply_text("Taklif va shikoyatlaringizni yozib yuboring.")
    elif text == "Kitob (testlar haqida)":
        await update.message.reply_text("📚 Testlar haqida kitob pullik. Narxi: 45 000 so'm. @Akmaljon_lab bilan bog'laning.")
    elif text == "Foydalanuvchi qo'shish":
        await update.message.reply_text("✅ Botdan foydalanishga muvaffaqiyatli ro'yxatdan o'tdingiz!")
    elif text == "Organizmda qanday o'zgarish?":
        await update.message.reply_text("📋 Organizmdagi o‘zgarish yoki shikoyatni yozing, sizga mos tahlillar tavsiya qilamiz.")
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

    app.run_polling()

# Dastur ishga tushuruvchi joy
if __name__ == "__main__":
    main()
