from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
# --- Hormon ma'lumotlari lug'ati ---
hormone_info = {}
# hormone_part1.py
# 1–17 gormon ma'lumotlari
hormone_info.update({
    "TSH": (
        "📊 Norma: 0.27–4.2 mIU/L\n"
        "🔻 Kamaysa: gipertiroidizm (Basedow-Graves)\n"
        "🔺 Oshganda: gipotiroidizm (Hashimoto)\n"
        "⚡ Belgilar: sovuqqa sezuvchanlik, charchoq, vazn ortishi, depressiya\n"
        "🧪 Tekshiruv: qalqonsimon bez faoliyati, autoimmun kasalliklar\n"
        "📈 Homiladorlikda nazorat talab qilinadi\n"
        "📉 Davolashda sintetik T4 bilan monitoring\n"
        "🩺 Qo‘shimcha: FT4 va FT3 bilan birga ko‘riladi"
    ),
    "Free T4": (
        "📊 Norma: 0.93–1.7 ng/dL\n"
        "🔻 Kamaysa: qalqonsimon bez yetishmovchiligi\n"
        "🔺 Oshganda: tireotoksikoz\n"
        "⚡ Belgilar: yurak urishi, asabiylik, vazn yo‘qotish\n"
        "🧪 Tekshiruv: qalqonsimon bez kasalliklari aniqlash\n"
        "📈 Homiladorlikda normasi o‘zgarishi mumkin\n"
        "📉 Sintetik T4 dozalashida nazorat qilinadi\n"
        "🩺 Qo‘shimча: TSH bilan birga baholash"
    ),
    "Free T3": (
        "📊 Norma: 2.0–4.4 pg/mL\n"
        "🔻 Kamaysa: gipotiroidizmda\n"
        "🔺 Oshganda: faollashgan tireotoksikoz\n"
        "⚡ Belgilar: asabiylik, terlash, yurak tez urishi\n"
        "🧪 Tekshiruv: qalqonsimon bez faoliyati monitoringi\n"
        "📈 Tireotoksikozda asosiy marker\n"
        "📉 Qalqonsimon bez shikastida kamayadi\n"
        "🩺 Qo‘shimча: TSH, FT4 bilan tekshirilsin"
    ),
    "Total T4": (
        "📊 Norma: 5.1–14.1 µg/dL\n"
        "🔻 Kamaysa: gipotiroidizm\n"
        "🔺 Oshganda: tireotoksikoz, estrogen ta’siri\n"
        "⚡ Belgilar: charchoq, metabolizm sekinlashuvi\n"
        "🧪 Tekshiruv: umumiy tireoid faoliyat\n"
        "📈 TBG ko‘payganda oshadi\n"
        "📉 Gipotiroidizmda pasayadi\n"
        "🩺 Qo‘shimча: FT4 bilan aniqlash"
    ),
    "Total T3": (
        "📊 Norma: 80–200 ng/dL\n"
        "🔻 Kamaysa: og‘ir kasalliklar, gipotiroidizm\n"
        "🔺 Oshganda: tireotoksikoz\n"
        "⚡ Belgilar: asabiylashish, yurak urishi\n"
        "🧪 Tekshiruv: tireoid kasalliklarida aniqlash\n"
        "📈 Estrogen o‘zgarishlarida oshadi\n"
        "📉 Euthyroid sick syndrome da kamayadi\n"
        "🩺 Qo‘shimча: FT3 bilan solishtiriladi"
    ),
    "Anti-TPO": (
        "📊 Norma: <35 IU/mL\n"
        "🔻 Kamaysa: normal holat\n"
        "🔺 Oshganda: Hashimoto, Basedow kasalligi\n"
        "⚡ Belgilar: qalqonsimon bez yallig‘lanishi\n"
        "🧪 Tekshiruv: autoimmun tireoidit baholash\n"
        "📈 Tireotoksikozda ko‘tariladi\n"
        "📉 Kam hollarda monitoring\n"
        "🩺 Qo‘shimча: Anti-TG bilan birga aniqlash"
    ),
    "Anti-TG": (
        "📊 Norma: <20 IU/mL\n"
        "🔻 Kamaysa: normal holat\n"
        "🔺 Oshganda: Hashimoto, Basedow\n"
        "⚡ Belgilar: qalqonsimon bez disfunktsiyasi\n"
        "🧪 Tekshiruv: autoimmun bez kasalliklari\n"
        "📈 Tireoglobulin darajasini baholash\n"
        "📉 Karcinoma monitoringida ishlatiladi\n"
        "🩺 Qo‘shimча: Anti-TPO bilan birgalikda"
    ),
    "Thyroglobulin": (
        "📊 Norma: 1.4–78.0 ng/mL\n"
        "🔻 Kamaysa: qalqonsimon bez olib tashlanganda\n"
        "🔺 Oshganda: qalqonsimon bez o‘smasi, tireoidit\n"
        "⚡ Belgilar: o‘sma alomatlari\n"
        "🧪 Tekshiruv: qalqonsimon bez monitoringi\n"
        "📈 Tiroglobulin antikorlari ham baholanishi kerak\n"
    ),
# hormone_part2.py
# 18–34 gormon ma'lumotlari
    "SHBG (Sex Hormone Binding Globulin)": (
        "📊 Norma: erkaklar 10–57 nmol/L, ayollar 18–144 nmol/L\n"
        "🔻 Kamaysa: insulin rezistentlikda\n"
        "🔺 Oshganda: estrogen darajasi oshishi\n"
        "⚡ Belgilar: testosteron ta’sir yo‘qolishi\n"
        "🧪 Tekshiruv: jinsiy gormon balansini baholash\n"
        "📈 PCOSda past bo‘lishi mumkin\n"
        "📉 Diabetda kamayadi\n"
        "🩺 Qo‘shimча: erkin testosterone bilan solishtirish"
    ),
    "DHT (Dihydrotestosterone)": (
        "📊 Norma: erkaklar 30–85 ng/dL\n"
        "🔻 Kamaysa: jinsiy rivojlanish buzilishi\n"
        "🔺 Oshganda: prostata giperplaziyasi\n"
        "⚡ Belgilar: soch to‘kilishi, akne\n"
        "🧪 Tekshiruv: androgen aktivligini baholash\n"
        "📈 Prostat bez kattaligida oshadi\n"
        "📉 Gipogonadizm belgilarini ko‘rsatadi\n"
        "🩺 Qo‘shimча: 5-alfa reduktaza faolligi bilan baholash"
    ),
    "Androstenedione": (
        "📊 Norma: erkaklar 40–150 ng/dL, ayollar 30–200 ng/dL\n"
        "🔻 Kamaysa: adrenal yetishmovchilik\n"
        "🔺 Oshganda: adrenal o‘sma, PCOS\n"
        "⚡ Belgilar: akne, tuklanish\n"
        "🧪 Tekshiruv: androgen sintezini baholash\n"
        "📈 PCOSda oshadi\n"
        "📉 Yetishmovchilikda kamayadi\n"
        "🩺 Qo‘shimча: DHEA-S bilan birga baholash"
    ),
    "Estradiol (E2)": (
        "📊 Norma: ayollar 12–166 pg/mL, erkaklar 10–40 pg/mL\n"
        "🔻 Kamaysa: menopauza, hipogonadizm\n"
        "🔺 Oshganda: estrogen o‘sma\n"
        "⚡ Belgilar: hayz sikl buzilishi\n"
        "🧪 Tekshiruv: jinsiy sog‘liqni baholash\n"
        "📈 Ovulyatsiya oldidan oshadi\n"
        "📉 Tuxumdon faoliyati pasaygani ko‘rsatadi\n"
        "🩺 Qo‘shimча: FSH va LH bilan birga tekshiriladi"
    ),
    "Estriol (E3)": (
        "📊 Norma: homiladorlikda 4–40 ng/mL\n"
        "🔻 Kamaysa: homila rivojlanish buzilishi\n"
        "🔺 Oshganda: ko‘p homilalik\n"
        "⚡ Belgilar: homila monitoringi\n"
        "🧪 Tekshiruv: homiladorlik xavfini baholash\n"
        "📈 Ko‘p homilalikda oshadi\n"
        "📉 Rivojlanish kechikishda kamayadi\n"
        "🩺 Qo‘shimча: PAPP-A bilan birga kuzatiladi"
    ),
    "Progesterone": (
        "📊 Norma: luteal fazada 5–20 ng/mL\n"
        "🔻 Kamaysa: homiladorlik xavfi\n"
        "🔺 Oshganda: homiladorlik tasdiqi\n"
        "⚡ Belgilar: hayz siklining buzilishi\n"
        "🧪 Tekshiruv: tuxumdon monitoringi\n"
        "📈 Homiladorlikda ko‘payadi\n"
        "📉 Luteal faza yetishmovchiligi bo‘lsa pasayadi\n"
        "🩺 Qo‘shimча: beta-HCG bilan kuzatiladi"
    ),
    "Prolactin": (
        "📊 Norma: ayollar 4.8–23.3 ng/mL, erkaklar 4.0–15.2 ng/mL\n"
        "🔻 Kamaysa: hipoprolaktinemiya\n"
        "🔺 Oshganda: giperprolaktinemiya\n"
        "⚡ Belgilar: galaktoreya, hayz siklining buzilishi\n"
        "🧪 Tekshiruv: gipofiz bezining faoliyatini baholash\n"
        "📈 Stress yoki homiladorlikda oshishi mumkin\n"
        "📉 Dopamin agonistlari bilan davolashda kamayadi\n"
        "🩺 Qo‘shimча: MRI gipofiz tekshiruvi zarur"
    ),
    "FSH": (
        "📊 Norma: ayollar (folikulyar faza) 3.5–12.5 IU/L, erkaklar 1.4–18.1 IU/L\n"
        "🔻 Kamaysa: hipogonadizm\n"
        "🔺 Oshganda: menopauza, tuxumdon yetishmovchiligi\n"
        "⚡ Belgilar: bepushtlik, hayz buzilishi\n"
        "🧪 Tekshiruv: reproduktiv salomatlikni baholash\n"
        "📈 Menopauzada fiziologik ravishda ko‘tariladi\n"
        "📉 Luteinizing Hormone bilan birga baholash kerak\n"
        "🩺 Qo‘shimча: Estradiol bilan birga ko‘riladi"
    ),
    "LH": (
        "📊 Norma: ayollar (folikulyar faza) 1.9–12.5 IU/L, erkaklar 1.7–8.6 IU/L\n"
        "🔻 Kamaysa: hipogonadotropik gipogonadizm\n"
        "🔺 Oshganda: ovulyatsiya, PCOS\n"
        "⚡ Belgilar: bepushtlik, hayz buzilishi\n"
        "🧪 Tekshiruv: tuxumdon va moyak funktsiyasini monitoring qilish\n"
        "📈 Ovulyatsiya vaqtida keskin oshadi\n"
        "📉 Gormon yetishmovchiligi belgisi bo‘lishi mumkin\n"
        "🩺 Qo‘shimча: FSH bilan nisbatda baholash zarur"
    ),
    "AMH (Anti-Müllerian Hormone)": (
        "📊 Norma: 1–10 ng/mL\n"
        "🔻 Kamaysa: tuxumdon zaxirasi kamayishi\n"
        "🔺 Oshganda: PCOS\n"
        "⚡ Belgilar: bepushtlik, ovulyatsiya muammolari\n"
        "🧪 Tekshiruv: tuxumdon rezervini aniqlash\n"
        "📈 Yosh bilan pasayadi\n"
        "📉 Fertilitet baholashda muhim marker\n"
        "🩺 Qo‘shimча: FSH va LH bilan birga ko‘riladi"
    ),
    "Inhibin B": (
        "📊 Norma: erkaklarda 80–400 pg/mL, ayollarda 20–340 pg/mL\n"
        "🔻 Kamaysa: spermatogenez buzilishi\n"
        "🔺 Oshganda: tuxumdon o‘smasi\n"
        "⚡ Belgilar: bepushtlik, jinsiy rivojlanish muammolari\n"
        "🧪 Tekshiruv: tuxumdon va moyak faoliyatini baholash\n"
        "📈 Follikulyar fazada aniqlanadi\n"
    ),
# hormone_part3.py
    "IGFBP-3": (
        "📊 Norma: yosh va jinsga qarab farq qiladi\n"
        "🔻 Kamaysa: o‘sish buzilishi\n"
        "🔺 Oshganda: o‘sish gormon ortiqligi\n"
        "⚡ Belgilar: anormal o‘sish\n"
        "🧪 Tekshiruv: IGF-1 bahosini aniqlash\n"
        "📈 Akromegaliyada oshadi\n"
        "📉 Bolalarda kamayadi\n"
        "🩺 Qo‘shimча: GH bilan birga baholash"
    ),
    "Adiponectin": (
        "📊 Norma: 5–30 µg/mL\n"
        "🔻 Kamaysa: semizlik, rezistentlik\n"
        "🔺 Oshganda: sog‘lom metabolik profil\n"
        "⚡ Belgilar: metabolik sindrom\n"
        "🧪 Tekshiruv: insulin sezgirligini baholash\n"
        "📈 Yog‘ to‘qimalarda oshadi\n"
        "📉 Diabetda kamayadi\n"
        "🩺 Qo‘shimча: leptin bilan solishtirish"
    ),
    "Leptin": (
        "📊 Norma: erkaklar 0.5–6 ng/mL, ayollar 4–25 ng/mL\n"
        "🔻 Kamaysa: semizlik va ortiqcha ochlik\n"
        "🔺 Oshganda: rezistentlik\n"
        "⚡ Belgilar: vazn ortishi\n"
        "🧪 Tekshiruv: metabolik sindrom\n"
        "📈 Semizlikda oshadi\n"
        "📉 Ozg‘inlarda kamayadi\n"
        "🩺 Qo‘shimча: insulin bilan birga baholash"
    ),
    "Oxytocin": (
        "📊 Norma: 1–10 pg/mL\n"
        "🔻 Kamaysa: ijtimoiy bog‘lanish pasayishi\n"
        "🔺 Oshganda: emizish jarayonida\n"
        "⚡ Belgilar: kayfiyat o‘zgarishi\n"
        "🧪 Tekshiruv: emotsional tizim\n"
        "📈 Tug‘ruqda oshadi\n"
        "📉 Stressda kamayadi\n"
        "🩺 Qo‘shimча: prolaktin bilan birga tekshiriladi"
    ),
    "Melatonin": (
        "📊 Norma: kechasi 10–80 pg/mL\n"
        "🔻 Kamaysa: uyqusizlik\n"
        "🔺 Oshganda: sirkadiyal ritm buzilishi\n"
        "⚡ Belgilar: uyqu buzilishi\n"
        "🧪 Tekshiruv: uyqu tekshiruvi\n"
        "📈 Tunda maksimal\n"
        "📉 Kunduzi past\n"
        "🩺 Qo‘shimча: kortizol bilan birga kuzatiladi"
    ),
    "Vasopressin (ADH)": (
        "📊 Norma: 1–13 pg/mL\n"
        "🔻 Kamaysa: diabet insipidus\n"
        "🔺 Oshganda: giponatremiya\n"
        "⚡ Belgilar: chanqash, ko‘p siydik\n"
        "🧪 Tekshiruv: suv balansini baholash\n"
        "📈 Stressda oshadi\n"
        "📉 DIHda pasayadi\n"
        "🩺 Qo‘shimча: natriy bilan kuzatiladi"
    ),
    "Relaxin": (
        "📊 Norma: homiladorlikda 0–1400 pg/mL\n"
        "🔻 Kamaysa: tug‘ruq muammolari\n"
        "🔺 Oshganda: bo‘g‘im bo‘shashuvi\n"
        "⚡ Belgilar: bo‘g‘im og‘rig‘i\n"
        "🧪 Tekshiruv: homiladorlik monitoringi\n"
        "📈 Trimestr oxirida oshadi\n"
        "📉 Tug‘ruqdan keyin kamayadi\n"
        "🩺 Qo‘shimча: estrogen bilan birga tekshiriladi"
    ),
    "Kisspeptin": (
        "📊 Norma: 0.3–2.0 ng/mL\n"
        "🔻 Kamaysa: kechikkan pubertat\n"
        "🔺 Oshganda: erta pubertat\n"
        "⚡ Belgilar: jinsiy rivojlanish\n"
        "🧪 Tekshiruv: pubertat baholash\n"
        "📈 GnRH stimulyatsiyasi\n"
        "📉 Yetishmovchilik pasayadi\n"
        "🩺 Qo‘shimча: LH/FSH bilan birga kuzatiladi"
    ),
    "Catecholamines (E, NE)": (
        "📊 Norma: E 0–140 pg/mL, NE 80–520 pg/mL\n"
        "🔻 Kamaysa: simpatik zaiflik\n"
        "🔺 Oshganda: feokromositoma\n"
        "⚡ Belgilar: gipertenziya, tachikardiya\n"
        "🧪 Tekshiruv: stress javobi\n"
        "📈 Stress holatida\n"
        "📉 Disfunktsiyada\n"
        "🩺 Qo‘shimча: plazma metanefrin bilan birga tekshiriladi"
    ),
    "Plasma Free Metanephrine & Normetanephrine": (
        "📊 Norma: metanefrin <0.5 nmol/L, normetanefrin <0.9 nmol/L\n"
        "🔻 Kamaysa: normal holat\n"
        "🔺 Oshganda: feokromositoma\n"
        "⚡ Belgilar: terlash, yurak urishi\n"
        "🧪 Tekshiruv: paraganglioma diagnostikasi\n"
        "📈 Tinch holatda ham yuqori bo‘lsa kasallikdan darak beradi\n"
        "📉 Normal holatda stressga javob sifatida oz o‘zgaradi\n"
        "🩺 Qo‘shimча: katekolaminlar bilan baholash"
    ),
    "17-OH Progesterone": (
        "📊 Norma: 0.2–1.3 ng/mL (ayollar, folikulyar faza)\n"
        "🔻 Kamaysa: kortizol ishlab chiqarish buzilishi\n"
        "🔺 Oshganda: tug‘ma adrenal giperplaziya\n"
        "⚡ Belgilar: jinsiy rivojlanish anomalilari\n"
        "🧪 Tekshiruv: adrenal buzilishlar skriningi\n"
        "📈 Tug‘ma giperplaziyada ko‘payadi\n")
        })

# Asosiy menyu tugmalari
def get_main_menu():
    keyboard = [
        ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"],
        ["Bioximiya haqida", "Klinika haqida"],
        ["IXLA va IFA tekshiruv farqi"],
        ["Biz bilan bog'lanish", "Admin bilan bog'lanish"],
        ["Tahlil natijalarini olish", "Taklif va shikoyatlar"],
        ["Kitob (Analizlar haqida to'liq ma'lumot)"],
        ["Botga foydalanuvchi qo'shish", "Sizni nima bezovta qilmoqda?"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Orqaga/Menu/Start tugmalari
def get_back_menu_start():
    return ReplyKeyboardMarkup(
        [["⬅️ Orqaga", "🏠 Menu", "🚀 Start"]],
        resize_keyboard=True
    )

# Tahlillar guruhlari
def get_analysis_menu():
    keyboard = [
        ["Gormonlar", "TORCH Paneli"],
        ["Onkomarkerlar", "Vitaminlar va Anemiya"],
        ["Kardiomarkerlar", "Koagulyatsiya markerlari"],
        ["Suyak metabolizmi", "Jigar fibrozi"],
        ["Buyrak funksiyasi", "Immunoglobulinlar"],
        ["Autoimmun panel", "Yuqumli kasalliklar"],
        ["Allergenlar", "Dori vositalarini nazorati"],
        ["Umumiy qon tahlillari", "Siydik tahlillari"],
        # ... boshqa guruhlar ...
        ["⬅️ Orqaga", "🏠 Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Gormonlar ro'yxati
def get_hormone_menu():
    keys = list(hormone_info.keys())
    keyboard = [keys[i:i+3] for i in range(0, len(keys), 3)]
    keyboard.append(["⬅️ Orqaga", "🏠 Menu"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n"
        "🔬 Biz zamonaviy IXLA texnologiyasi bilan tahlillarni taqdim etamiz.\n"
        "Manzil va kontaktlar uchun pastdagi menyudan tanlang.",
        reply_markup=get_main_menu()
    )

# Tugma bosilishlari uchun handler
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Asosiy guruhlar
    if text == "Tahlillar haqida ma'lumot":
        await update.message.reply_text(
            "Quyidagi tahlil guruhlaridan birini tanlang:",
            reply_markup=get_analysis_menu()
        )

    # Gormonlar bo'limi
    elif text == "Gormonlar":
        await update.message.reply_text(
            "Quyidagi gormon testlaridan birini tanlang:",
            reply_markup=get_hormone_menu()
        )

    # Ma'lumot beringan gormon nomi
    elif text in hormone_info:
        await update.message.reply_text(
            hormone_info[text],
            reply_markup=get_back_menu_start()
        )

    # Orqaga yoki Menu
    elif text in ["⬅️ Orqaga", "🏠 Menu"]:
        await update.message.reply_text(
            "Asosiy menyuga qaytdingiz.",
            reply_markup=get_main_menu()
        )

    # Start
    elif text == "🚀 Start":
        await start(update, context)

    # Boshqa tugmalar...
    else:
        await update.message.reply_text(
            "Iltimos, menyudan tanlang.",
            reply_markup=get_back_menu_start()
        )

# Bot ishga tushirish
def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Bot token topilmadi. .env faylga TOKEN kiriting.")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.run_polling()

if __name__ == "__main__":
    main()


