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
hormone_info = {
    "O‘sish gormoni (GH)": {
        "Normasi": "Bolalarda: 10–50 ng/mL; Kattalarda: 0–10 ng/mL",
        "Oshganda": "Giperpituitarizm (akromegaliya kattalarda, gigantizm bolalarda)",
        "Kamayganda": "Gipopituitarizm (o‘sish gormoni yetishmovchiligi, bolalarda bo‘y o‘sishi sustligi)",
        "Organizmdagi belgilari": "Yuqori darajada – yuz va qo‘l-oyoqlarning haddan tashqari o‘sishi, ichki organlar kattalashishi, qo‘pol facial xususiyatlar; Past darajada – bolalarda bo‘y o‘smasligi, kattalarda mushak va suyak zaifligi, yog‘ to‘planishi va energiya yetishmovchiligi",
        "Qachon tekshirish kerak": "Bolalarda bo‘y o‘sishi sekinlashganda, kattalarda mushak kuchsizligi va suyak mo‘rtlashishi kuzatilganda, akromegaliya yoki gigantizm alomatlari paydo bo‘lsa, semizlik va metabolik muammolar sababini aniqlashda"
    },
    "Prolaktin (PRL)": {
        "Normasi": "Ayollarda: 4,8–23,3 ng/mL; Homiladorlarda: 34–386 ng/mL; Erkaklarda: 4,0–15,2 ng/mL",
        "Oshganda": "Giperprolaktinemiya (gipofiz o‘smasi yoki boshqa sabablar)",
        "Kamayganda": "Gipoprolaktinemiya (kam uchraydi, laktatsiya yetishmovchiligi)",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda sut ajralishi (galaktoreya), hayz ko‘rmaslik yoki bepushtlik, jinsiy aloqa qiziqishi pasayishi, erkaklarda jinekomastiya; Past darajada – emizishda qiyinchilik, charchoq va kayfiyat tushkunligi (gipotireozga o‘xshash)",
        "Qachon tekshirish kerak": "Ayollarda hayz sikli buzilganda yoki bepushtlikda, erkaklarda jinsiy qobiliyat pasayganda yoki ko‘krak to‘qimasi kengayganda, emizuvchi onalarda sut kelishi sust bo‘lsa"
    },
    "Tirotrop gormoni (TSH)": {
        "Normasi": "0,4–4,0 mIU/L",
        "Oshganda": "Gipotireoz (qalqonsimon bez yetishmovchiligi)",
        "Kamayganda": "Gipertireoz (qalqonsimon bez haddan tashqari faolligi)",
        "Organizmdagi belgilari": "Yuqori darajada – lanjlik, vazn ortishi, sovuqsevarlik, quruq teri, depressiya (gipotireoz alomatlari); Past darajada – tez yurak urishi, vazn yo‘qotish, asabiylik, haddan tashqari terlash, ko‘zlarning bo‘rtib chiqishi (Basedov kasalligi alomatlari)",
        "Qachon tekshirish kerak": "Qalqonsimon bez kasalliklari alomatlari (masalan, holsizlik, semirish yoki ozib ketish, bo‘yinda bo‘rtma) paydo bo‘lganda, metabolik buzilishlarda, homiladorlik rejalashtirilganda"
    },
    "Adrenokortikotrop gormon (ACTH)": {
        "Normasi": "Ertalab: 10–60 pg/mL; Kechqurun: 5–20 pg/mL",
        "Oshganda": "Kuşing kasalligi (giperkortisolizm, ACTH ortiqcha ishlab chiqarilishi)",
        "Kamayganda": "Adisson kasalligi (gipokortisolizm, ACTH yetishmasligi)",
        "Organizmdagi belgilari": "Yuqori darajada – yuz va qorin sohasida yog‘ to‘planishi, yuqori qon bosimi, mushak zaifligi, suyaklar mo‘rtlashuvi (Kortizol oshishi belgilar); Past darajada – doimiy charchoq, terining bronza rangga kirishi, past qon bosimi, vazn yo‘qotish (Kortizol yetishmovchiligi belgilar)",
        "Qachon tekshirish kerak": "Qonda kortizol darajasi g‘ayrioddiy yuqori yoki past bo‘lsa, Kuşing yoki Adisson kasalligidan shubha qilinsa (masalan, teri pigmentatsiyasi o‘zgarishi, qon bosimi o‘zgarishlari, stressga nisbatan nomutanosib reaksiyalar)"
    },
    "Follikulostimulyatsiya gormoni (FSH)": {
        "Normasi": "Ayollarda (hayz bosqichiga qarab): folikulyar faza 3,5–12,5 mIU/mL, ovulyatsiya 4,7–21,5, luteal faza 1,7–7,7; Menopauzada: 25,8–134,8 mIU/mL; Erkaklarda: 1,5–12,4 mIU/mL",
        "Oshganda": "Ayollarda ovulyatsiya buzilishi yoki erta menopauza, polikistik tuxumdon sindromi (PCOS); Erkaklarda gipergonadotrop hipogonadizm (testosteron pasayishi bilan bepushtlik); Gipofiz bezining giperaktivligi",
        "Kamayganda": "Gipogonadizm (jinsiy bezlar faoliyatining sustligi); Gipotalamik yoki gipofiz yetishmovchiligi; Semizlik va metabolik sindrom",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda hayz ko‘rmaslik yoki infertilitet, erta klimaks belgilari (issiq bosishlar); erkaklarda urug‘ ishlab chiqarish pasayishi; Past darajada – jinsiy yetilishning kechikishi, ayollarda ovulyatsiya yo‘qligi, erkaklarda sperma miqdori kamayishi va bepushtlik",
        "Qachon tekshirish kerak": "Hayz sikli muntazam bo‘lmasa, bepushtlik muammolarida (ham erkak, ham ayolda), ayollarda erta menopauza alomatlarida yoki erkaklarda testosteron yetishmovchiligi belgilari kuzatilganda"
    },
    "Lyuteinizatsiya gormoni (LH)": {
        "Normasi": "Ayollarda: folikulyar faza 1,9–12,5 mIU/mL, ovulyatsiya fazasi 8,7–76,3, luteal faza 0,5–16,9, menopauza 15,9–54,0 mIU/mL; Erkaklarda: 1,7–8,6 mIU/mL",
        "Oshganda": "Ayollarda polikistik tuxumdon sindromi (PCOS) yoki erta menopauza; Erkaklarda gipergonadotrop hipogonadizm (past testosteron bilan bepushtlik); Gipofiz o‘smalari",
        "Kamayganda": "Gipogonadotrop hipogonadizm (gipotalamus/gipofiz yetishmovchiligi); Gormonal buzilishlar; Jinsiy balog‘atning kechikishi",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda hayz sikli buzilishi yoki ovulyatsiya yo‘qligi, erkaklarda jinsiy funksiyalar pasayishi; Past darajada – o‘smirlikda jinsiy yetilish kechikishi, reproduktiv qobiliyatning pasayishi, umumiy energiya va jinsiy istakning kamayishi",
        "Qachon tekshirish kerak": "Ayollarda hayz sikli va ovulyatsiya muammolarida, bepushtlikda, erkaklarda testosteron pastligi yoki jinsiy rivojlanish muammolari kuzatilganda"
    },
    "Melanotsit-stimulyatsiya gormoni (MSH)": {
        "Normasi": "Aniq belgilangan norma yo‘q (yosh va holatga bog‘liq, odatda maxsus tekshirilmaydi)",
        "Oshganda": "MSH giperproduksiyasi (masalan, Adisson kasalligida ACTH bilan birga oshadi) – teri hiperpigmentatsiyasi",
        "Kamayganda": "MSH yetishmovchiligi (masalan, gipofiz yetishmovchiligida) – teri pigmentatsiyasi kamayishi",
        "Organizmdagi belgilari": "Yuqori darajada – terining to‘q tusga kirishi, tozalashgan joylar paydo bo‘lishi (quyuq pigmentatsiya); Past darajada – teri oqarishi yoki odatdagidan oqaroq rangda bo‘lishi, quyoshga sezgirlik oshishi",
        "Qachon tekshirish kerak": "MSH darajasi odatda bevosita tekshirilmaydi; teri rangidagi keskin o‘zgarishlar (sababsiz qorayish yoki oqarish) kuzatilsa, bu gipofiz yoki buyrak usti bezlari kasalliklari bo‘yicha qo‘shimcha tekshiruvlarni talab qiladi"
    },
    "Oksitotsin": {
        "Normasi": "Qonda doimiy miqdori uchun aniq norma yo‘q (faoliyatiga qarab epizodik ajraladi)",
        "Oshganda": "Oksitotsin ortiqcha ajralishi odatda patologiya emas (mehnat paytida va emizishda fiziologik ko‘tariladi)",
        "Kamayganda": "Oksitotsin yetishmovchiligi (masalan, homiladorlikda mehnat faoliyatining sustligi yoki laktatsiya muammolari)",
        "Organizmdagi belgilari": "Yuqori darajada – bachadon qisqarishlari kuchayishi (tug‘ruq paytida), ko‘krakdan sut ajralishi osonlashishi; Past darajada – tug‘ruq vaqtida bachadon qisqarishlarining sustligi, tug‘ilgandan keyin bachadonning sekin qisqarishi va ko‘krak suti ajrala olmasligi",
        "Qachon tekshirish kerak": "Oksitotsin darajasi rutinga kiritilmagan; agar tug‘ruq kuchini oshirish yoki laktatsiya muammolarini baholash kerak bo‘lsa, klinik belgilarga qarab baholanadi (zarurat bo‘lsa, oksitotsin stimulatsiyasi bilan sinov o‘tkaziladi)"
    },
    "Vazopressin (ADH)": {
        "Normasi": "1–5 pg/mL (qonda, gidratatsiya holatiga bog‘liq holda o‘zgaradi)",
        "Oshganda": "Antidiuretik gormon sindromi (SIADH) – ADH me’yordan ortiq (bosh miya o‘smasi, o‘pka kasalliklari sababli)",
        "Kamayganda": "Diabet insipidus – ADH yetishmasligi (gipofiz yoki buyrak kasalligi tufayli)",
        "Organizmdagi belgilari": "Yuqori darajada – suyuqlik organizmda ushlanib qoladi, siydik kamayadi, qonda natriy past (lohaslik, bosh aylanishi, tutqanoqlar); Past darajada – ko‘p miqdorda siydik ajralishi va doimiy chanqoq (dehidratatsiya, qon bosimi pasayishi, quruq teri va shilliq qavatlar)",
        "Qachon tekshirish kerak": "Qattiq chanqoqlik va ko‘p siydik ajralishi kuzatilsa (diabet insipidusdan shubha), yoki qonda natriy darajasi tushib ketgan bo‘lsa va suyuqlik tutilishi alomatlari bo‘lsa (SIADH shubhasi)"
    },

    "Triyodtironin (T3)": {
        "Normasi": "Umumiy T3: 80–200 ng/dL; Erkin T3: 2,3–4,2 pg/mL",
        "Oshganda": "Gipertireoz (tireotoksikoz, qalqonsimon bez giperfaolligi)",
        "Kamayganda": "Gipotireoz (qalqonsimon bez yetishmovchiligi)",
        "Organizmdagi belgilari": "Yuqori darajada – yurak urishi tezlashishi (taxikardiya), asabiylik, xavotir, haddan tashqari terlash, vaznning tez yo‘qolishi, bo‘yinda qalqonsimon bez kattalashishi (bag‘riksillik); Past darajada – doimiy charchoq, sustlik, terining quruqligi, soch to‘kilishi, yurak urishining sekinlashishi, vazn ortishi, sovuqqa nisbatan sezgirlik",
        "Qachon tekshirish kerak": "Qalqonsimon bez faoliyati buzilishi belgilari paydo bo‘lganda (masalan, tireotoksikoz yoki hipotireozdan shubha qilinganda), qalqonsimon bezdagi nodullar yoki kattalashish baholanganda"
    },
    "Tetrayodtironin (T4, tiroksin)": {
        "Normasi": "Umumiy T4: 4,5–12,5 µg/dL; Erkin T4: 0,8–2,0 ng/dL",
        "Oshganda": "Gipertireoz (qalqonsimon bez haddan tashqari faol ishlashi)",
        "Kamayganda": "Gipotireoz (qalqonsimon bez yetarlicha faol ishlamasligi)",
        "Organizmdagi belgilari": "Yuqori darajada – yurak urishining tezlashishi, asabiylik va qo‘l-qo‘llarning titrashi, issiq bosishi va kuchli terlash, mushak zaifligi, qalqonsimon bezning kattalashishi (diffuz zoba); Past darajada – energiya yetishmasligi, sovuqsevarlik, diqqatni jamlay olmaslik, kayfiyat tushkunligi, vazn ortishi, teri qurishi va soch to‘kilishi",
        "Qachon tekshirish kerak": "Qalqonsimon bez faoliyatida o‘zgarishlar (masalan, bo‘yinda shish, gormonlar nomutanosibligi) kuzatilsa, metabolik kasalliklar va semizlik sabablarini aniqlashda, tireoidit yoki qalqonsimon bez tugunlari mavjud bo‘lsa"
    },
    "Kalsitonin": {
        "Normasi": "Erkaklarda: <8 pg/mL; Ayollarda: <5 pg/mL",
        "Oshganda": "Medullyar qalqonsimon bez raki (C-hujayra karsinomasida kalsitonin oshadi); Qalqonsimon bezning medullar o‘smasi; Ba’zi o‘pka va sut bezi o‘smalari",
        "Kamayganda": "Kalsitonin darajasining kamayishi klinik jihatdan muhim emas (qalqonsimon bez C-hujayralari faoliyatining pasayishi)",
        "Organizmdagi belgilari": "Yuqori darajada – qonda kalsiy miqdori pasayishi mumkin (qo‘l-oyoq uvishishi, mushak kramplari), medullyar rakkka xos alomatlar (bo‘yinda tugun, diareya, yuzda qizarish); Past darajada – aniq klinik simptomlar yo‘q, lekin qonda kalsiy me’yordan biroz oshishi mumkin",
        "Qachon tekshirish kerak": "Qalqonsimon bezda shubhali tugunlar aniqlansa (medullyar rakni istisno qilish uchun), medullyar qalqonsimon bez raki bilan og‘rigan bemorlarning yaqin qarindoshlarida skrining sifatida"
    },
    "Kortizol": {
        "Normasi": "Ertalab: 5–25 µg/dL; Kechqurun: 3–10 µg/dL",
        "Oshganda": "Kuşing sindromi (giperkortisolizm, kortizol me’yordan ortiq)",
        "Kamayganda": "Adisson kasalligi (gipokortisolizm, kortizol yetishmovchiligi)",
        "Organizmdagi belgilari": "Yuqori darajada – qorin va yuz (\"oy-simon\" yuz) sohalarida yog‘ to‘planishi, qon bosimi oshishi, mushaklarning zaiflashuvi, suyaklarning mo‘rtlashuvi, immunitet pasayishi (infeksiyalarga moyillik); Past darajada – doimiy holsizlik, vazn tashlash, past qon bosimi, terining quyuq tus olishi (pigmentatsiya), ishtahaning yo‘qolishi va tuzga o‘chlik",
        "Qachon tekshirish kerak": "Stressga nisbatan g‘ayrioddiy klinik reaksiyalar paydo bo‘lsa (masalan, yuqori qon bosimi, qandli diabet yomonlashuvi), Kuşing yoki Adisson kasalligidan shubha qilinganida (semizlik, yuqori qon bosimi va qand ko‘tarilishi yoki aksincha g‘ayrioddiy charchoq, past bosim va pigmentatsiya), gormonal nomutanosiblik belgilari kuzatilganda"
    },
    "Aldosteron": {
        "Normasi": "Yotgan holatda: 3–16 ng/dL; Tik turganda: 7–30 ng/dL",
        "Oshganda": "Giperaldosteronizm (Conn sindromi – aldosteronning ortiqcha ishlab chiqarilishi)",
        "Kamayganda": "Gipoaldosteronizm (aldosteron yetishmovchiligi)",
        "Organizmdagi belgilari": "Yuqori darajada – arterial gipertenziya (qon bosimining doimiy oshishi), qonda kaliy darajasining pasayishi (gipokalemiya, bundan mushaklarda kuchsizlanish va kramplar), ko‘p siyish va doimiy chanqoq; Past darajada – arterial gipotenziya (past qon bosimi), organizmda tuzga ehtiyoj oshishi, suvsizlanish, holsizlik va yurak ritmining buzilishi",
        "Qachon tekshirish kerak": "Qon bosimi doimiy ravishda yuqori bo‘lsa (gipertenziya davolashga qaramay tushmasa) yoki aksincha tushib ketsa, qonda kaliy darajasi tushib ketgan bo‘lsa, buyrak usti bezlari kasalliklariga (masalan, Conn sindromi yoki Adisson) shubha bo‘lsa"
    },
    "Adrenalin (epinefrin)": {
        "Normasi": "Yotgan holatda ≈0–100 pg/mL; Faollik va stressga qarab sezilarli o‘zgaradi",
        "Oshganda": "Feokromotsitoma (buyrak usti bezi o‘smalari adrenalinni ko‘p ajratadi)",
        "Kamayganda": "Adrenal yetishmovchiligi (Adisson kasalligi)",
        "Organizmdagi belgilari": "Yuqori darajada – paroksizmal holatda yuqori qon bosimi xurujlari, yurak urishi tezlashuvi, terlash, qo‘rquv va vahima hissi, bosh og‘rigi (feokromotsitoma xurujlari); Past darajada – lohaslik, doimiy charchoq, past qon bosimi va stress holatlarida javobning sustligi (buyrak usti bezi yetishmovchiligi)",
        "Qachon tekshirish kerak": "Tanaffusli yuqori qon bosimi xurujlari, yurak urishi va terlashi kuzatilsa (feokromotsitomadan shubhalanganda); shuningdek, Adisson kasalligiga gumon bo‘linsa (masalan, stressga dosh berolmaslik, past qon bosimi va giperpigmentatsiya bilan namoyon bo‘lsa)"
    },
    "Noradrenalin (norepinefrin)": {
        "Normasi": "Yotgan holatda ≈100–300 pg/mL (organizmdagi holatga bog‘liq, stressda oshadi)",
        "Oshganda": "Feokromotsitoma (ayniqsa noradrenalin ajratuvchi o‘sma)",
        "Kamayganda": "Avtonom asab tizimi yetishmovchiligi yoki adrenal yetishmovchilik (og‘ir holatlarda)",
        "Organizmdagi belgilari": "Yuqori darajada – doimiy yuqori qon bosimi, bosh og‘rig‘i, yurak urishi tezlashuvi, oqarib ketish va asabiylik; Past darajada – qon bosimining pasayishi, ayniqsa o‘rnidan turganda bosh aylanib yiqilib qolish (ortostatik gipotenziya), loqaydlik va kuchsizlik",
        "Qachon tekshirish kerak": "Sababi noma’lum yuqori qon bosimi va uning xurujlari kuzatilsa (feokromotsitomadan shubha), yoki avtonom disfunksiya belgilari – o‘rnidan turganda bosim tushib ketishi, vegetativ asab tizimi kasalliklari – kuzatilsa"
    },
    "Dehidroepiandrosteron (DHEA)": {
        "Normasi": "Yoshga bog‘liq: 20–30 yoshlarda eng yuqori (taxminan 280–640 µg/dL), undan so‘ng yoshi o‘tgan sayin pasayadi",
        "Oshganda": "Adrenal androgen giperproduksiyasi (buyrak usti bezining o‘smasi yoki giperplaziyasi); Ayollarda – polikistik tuxumdon sindromi (DHEA sulfat oshishi); Erkaklarda odatda klinik ta’siri sezilarli emas",
        "Kamayganda": "Adrenal yetishmovchilik (Adisson kasalligi); Yoshi o‘tishi bilan tabiiy ravishda kamayadi",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda ortiqcha tuklanish (girsutizm), ug‘revoy toshma (acne), hayz sikli buzilishi, yosh o‘smirlarda erta balog‘at; Past darajada – umumiy holsizlik, libido pasayishi, mushak massasi kamayishi va suyak sichrashi (ayniqsa yoshi katta odamlarda)",
        "Qachon tekshirish kerak": "Ayollarda gormonlar nomutanosibligi va virilizatsiya alomatlari (ortiqcha tuk o‘sishi, akne) kuzatilsa, bolalarda balog‘at davri o‘zgarishlari me’yordan oldin yoki keyin bo‘lsa, Adisson kasalligidan shubha qilinganda"
    },
    "Insulin": {
        "Normasi": "Och qoringa: 3–25 µIU/mL (qon zardobida)",
        "Oshganda": "Giperinsulinemiya (masalan, insulinoma – oshqozon osti bezi o‘smasi; 2-tip qandli diabetda insulin rezistentligi bilan)",
        "Kamayganda": "Insulin yetishmovchiligi (1-tip qandli diabet yoki  pankreatik beta-hujayralar shikastlanishi)",
        "Organizmdagi belgilari": "Yuqori darajada – qonda qand darajasi keskin tushib ketishi (gipoglikemiya: terlash, qo‘l qaltirashi, yurak urishi, hushdan ketish holi); Past darajada – qonda qand miqdori oshishi (giperlikemiya: chanqoqlik, ko‘p siyish, vazn yo‘qotish, surunkali charchoq)",
        "Qachon tekshirish kerak": "Gipoglikemiya epizodlari sababi aniqlanmasa (insulinoma shubhasi), 1-tip va 2-tip qandli diabet tashxisi va kuzatuvida, insulin rezistentligi sindromi baholashda"
    },
    "Glyukagon": {
        "Normasi": "50–150 pg/mL (och qoringa)",
        "Oshganda": "Glukagonoma (oshqozon osti bezining alfa-hujayra o‘smasi); 1-tip qandli diabet (insulin yetishmaganda kompensator oshishi mumkin)",
        "Kamayganda": "Pankreasning surunkali kasalliklari (masalan, surunkali pankreatit) yoki insulin gipersekresiyasi",
        "Organizmdagi belgilari": "Yuqori darajada – qonda glyukoza oshishi (giperlikemiya, diabet alomatlari), terida qizil toshmalar (glukagonoma belgisi – nekrolitik migrirlovchi eritema), ishtaha oshishi; Past darajada – gipoglikemiya epizodlariga moyillik (kamqonlik, holsizlik, ter bosishi) insulin ortiqligida",
        "Qachon tekshirish kerak": "Noma’lum kelib chiqishi qandli diabet belgilari va teri toshmalari bo‘lsa (glukagonomadan shubha), pankreatik gormonlar faoliyatini baholashda, og‘ir gipoglikemiya epizodlarida (giperoinsulinizmni tasdiqlash uchun, glyukagon javobini ko‘rish maqsadida)"
    },
    "Somatostatin": {
        "Normasi": "Taxminan 10–30 pg/mL (aniq norma belgilanmagan, ovqatlanishga bog‘liq o‘zgaradi)",
        "Oshganda": "Somatostatinoma (oshqozon osti bezi yoki ichak o‘smasi somatostatin ko‘p ajratadi)",
        "Kamayganda": "Amalda klinik ahamiyatga ega emas (somatostatinning pastligi alohida kasallik sifatida kuzatilmaydi)",
        "Organizmdagi belgilari": "Yuqori darajada – qandli diabet belgilari (somatostatin insulin sekretsiyasini to‘xtatadi), yog‘larning o‘zlashishi buzilishi (jig‘ildon qaynashi, diareya), xoletsistit va o‘t toshi (o‘t pufagi qisqarishi susayadi); Past darajada – aniq belgilarga olib kelmaydi, oshqozon-ichak sekresiyasi va gormonlar me’yorda oshishi mumkin",
        "Qachon tekshirish kerak": "Somatostatinoma juda nodir kasallik; surunkali diareya, vazn yo‘qotish, qandli diabet va o‘t toshlari kombinatsiyasi kuzatilsa, shifokor ushbu gormonni tekshirishni tavsiya qilishi mumkin"
    },
    "Pankreatik polipeptid (PP)": {
        "Normasi": "Siydikda 0–300 pg/mL (och qoringa, qiymatlar individualligi yuqori)",
        "Oshganda": "Pankreatik polipeptidoma (oshqozon osti bezi o‘smasi); Ba’zi gastrointestinal kasalliklar",
        "Kamayganda": "Klinik axamiyatga ega emas (me’yordan past PP holati aniq sindrom keltirib chiqarmaydi)",
        "Organizmdagi belgilari": "Yuqori darajada – ishtahaning pasayishi, ovqatdan keyin qorinda noqulaylik, me’da osti bezi fermentlari ajralishining kamayishi tufayli hazm bo‘lishning buzilishi; Past darajada – aniq simptomlar yo‘q (oshqozon osti bezi sekresiyasining biroz ortishi bo‘lishi mumkin)",
        "Qachon tekshirish kerak": "Ushbu gormon odatda klinikada tez-tez tekshirilmaydi; oshqozon osti bezining endokrin o‘smalaridan shubha qilinganda yoki murakkab hazm qilish buzilishlarini tadqiq qilish doirasida PP darajasini tekshirish mumkin"
    },

    "Testosteron": {
        "Normasi": "Erkaklarda: 300–1000 ng/dL; Ayollarda: 15–70 ng/dL (fertil yoshda, hayz sikliga bog‘liq o‘zgaradi)",
        "Oshganda": "Giperandrogenizm: Erkaklarda anabolik steroidlarni suiiste’mol qilish; Ayollarda polikistik tuxumdon sindromi (PKOS) yoki androgen ajratuvchi o‘sma",
        "Kamayganda": "Hipogonadizm: Erkaklarda moyak yetishmovchiligi (masalan, Klinefelter sindromi) yoki hipofiz yetishmovchiligi; Ayollarda tuxumdon yetishmovchiligi (masalan, menopauza yoki tuxumdonlar olib tashlangan)",
        "Organizmdagi belgilari": "Yuqori darajada – erkaklarda husnbuzar va tajovuzkorlik ortishi, prostata bezi kattalashuvi; ayollarda erkaklarga xos belgilar (ortiqcha tuklar, ovoz dag‘allashishi, hayz to‘xtashi); Past darajada – erkaklarda jinsiy zaiflik, urug‘ kamligi, mushak massasi pasayishi, suyaklar mo‘rtlashuvi; ayollarda libido pasayishi, suyak sichrashi ortishi",
        "Qachon tekshirish kerak": "Erkaklarda jinsiy funktsiya buzilganda, bepushtlikda yoki kechikkan balog‘atda; Ayollarda virilizatsiya (erkaklik belgilarining paydo bo‘lishi) kuzatilganda, menstrual sikl buzilganda yoki bepushtlik muammolarida"
    },
    "Estrogenlar (estradiol va boshqalar)": {
        "Normasi": "Ayollarda (estradiol): follikulyar fazada ~30–120 pg/mL, ovulyatsiya paytida 130–370 pg/mL, luteal fazada 70–250 pg/mL, menopauzada <30 pg/mL; Erkaklarda: 10–50 pg/mL",
        "Oshganda": "Hiperestrogenemiya: Ayollarda estrogen ajratuvchi o‘sma (masalan, granulyoza hujayrali o‘sma) yoki semizlik; Erkaklarda jigar tsirrozi (estrogen metabolizmi buziladi) yoki estrogen ajratuvchi o‘sma",
        "Kamayganda": "Gipoestrogenemiya: Ayollarda tuxumdon yetishmovchiligi (masalan, muddatidan oldin menopauza yoki Turner sindromi); Erkaklarda testikulyar feminizatsiya sindromi kabi kam holatlar",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda hayz sikli buzilishi (masalan, me’yoridan ortiq qon ketishi), bachadon miomalari va ko‘krak o‘smasi xavfi oshishi; erkaklarda jinekomastiya (ko‘krak bezlarining kattalashishi), jinsiy funksiyalar pasayishi; Past darajada – ayollarda hayzning to‘xtashi, issiq bosishlar, qin quruqligi va suyaklarning mo‘rtlashishi (menopauza simptomlari); erkaklarda urug‘lanish qobiliyatining pasayishi va osteoporoz xavfining ortishi",
        "Qachon tekshirish kerak": "Ayollarda hayz sikli uzilib qolsa yoki bepushtlikda (masalan, muddatidan avval klimaks shubhasida), menopauza alomatlari og‘ir kechsa; Erkaklarda sababsiz jinekomastiya paydo bo‘lsa yoki jinsiy zaiflik va bepushtlik holatlarida"
    },
    "Progesteron": {
        "Normasi": "Ayollarda: follikulyar fazada <1 ng/mL, luteal fazada 5–20 ng/mL; Homiladorlik 1-trimestrida: ~11–44 ng/mL",
        "Oshganda": "Giperprogesteronemiya: Odatda homiladorlikda fiziologik; Homiladorlikdan tashqari – sariq tana kistalari yoki ba’zi buyrak usti bezlari o‘smalarida",
        "Kamayganda": "Gipoprogeteronemiya: Luteal faza yetishmovchiligi (ayollarda urug‘lanish qiyinligi, erta homiladorlik tushishi xavfi); Bachadondan tashqari homiladorlik",
        "Organizmdagi belgilari": "Yuqori darajada – ko‘krak sezuvchanligi, bo‘ksa va qorin sohasida suyuqlik ushlanishi, kayfiyat o‘zgaruvchanligi (odatda homiladorlik belgilariga o‘xshash); Past darajada – hayz oldi qonli ajralmalar, hayz siklining qisqarishi, homiladorlik davom etishida muammo (agar homiladorlik bo‘lsa, erta tushish belgilari: qorindagi og‘riq, qonli ajralma)",
        "Qachon tekshirish kerak": "Ayollarda homilador bo‘lolmaslik va takroriy homila tushishlarida (luteal faza yetarlimi yoki yo‘qligini bilish uchun), hayz sikli buzilishlarida (luteal faza qisqa bo‘lsa) yoki homiladorlikni erta bosqichida homon darajalarini baholash uchun"
    },
    "Inhibin": {
        "Normasi": "Ayollarda: hayz davriga bog‘liq (ovulyatsiya oldi davrida Inhibin B ~40–100 pg/mL, menopauzada juda past); Erkaklarda: 80–270 pg/mL (Inhibin B, normal spermatogenezda)",
        "Oshganda": "Ayollarda – granulyoza hujayrali o‘sma (inhibin ajratuvchi tuxumdon o‘smalari); Erkaklarda – ayrim testikulyar o‘smalar inhibin ishlab chiqishi mumkin",
        "Kamayganda": "Ayollarda – tuxumdon zahirasining kamayishi (masalan, klimaks yaqinlashganda yoki tuxumdon yetishmovchiligida inhibin B pasayadi); Erkaklarda – spermatogenez buzilishi (past Inhibin B, masalan, cryptorchidizm yoki Klinefelter sindromida)",
        "Organizmdagi belgilari": "Yuqori darajada – ayollarda hayz siklining buzilishi yoki bepushtlik (tuxumdon o‘smasi sababli); erkaklarda belgilar aniq emas, lekin bepushtlikka olib keluvchi asosiy kasallik belgilari bo‘lishi mumkin; Past darajada – ayollarda tug‘ish qobiliyatining pasayishi, hayzlar oralig‘ining qisqarishi yoki klimaks alomatlari; erkaklarda urug‘ miqdori va sifati pasayishi",
        "Qachon tekshirish kerak": "Ayollarda bepushtlik tekshiruvlarida (ayniqsa tuxumdon zahirasini baholashda, Inhibin B darajasi), tuxumdonning granulyoza hujayrali o‘smalariga gumon qilinganda; Erkaklarda bepushtlik tekshiruvlarida spermatogenez ko‘rsatkichlarini bilish maqsadida"
    },
    "Relaksin": {
        "Normasi": "Homilador bo‘lmaganlarda juda past; Homiladorlikda 2-3-trimestrlarda sezilarli oshadi (eng yuqori darajasi tug‘ruq oldidan)",
        "Oshganda": "Homiladorlik paytida me’yorida oshadi (ayniqsa ko‘p homilali homiladorlikda relaksin darajasi balandroq bo‘lishi mumkin); Homiladorlikdan tashqari patologik oshishi kuzatilmaydi",
        "Kamayganda": "Homiladorlikda past bo‘lsa – platsentar funksiyaning yetishmovchiligi mumkin; Homiladorlikdan tashqari – normada juda past darajada bo‘ladi",
        "Organizmdagi belgilari": "Yuqori darajada – bo‘g‘imlarning bo‘shashuvi va boylamlarning yumshashi (homiladorlik paytida tos suyaklari va bachadon bo‘yinchasini tug‘ruqqa tayyorlaydi); Past darajada – homiladorlikda relaksin past bo‘lsa, tug‘ruq jarayoni sust kechishi yoki muddatidan oldin tug‘ruq xavfi oshishi mumkin",
        "Qachon tekshirish kerak": "Relaksin odatda maxsus tekshirilmaydi; faqat ilmiy-tadqiqot doirasida yoki homiladorlik asoratlarida (masalan, muddatidan oldin tug‘ruqqa moyillikda) o‘rganilishi mumkin"
    },
    "Melatonin": {
        "Normasi": "Kunduzi <20 pg/mL; Tun vaqti (tun yarimida) ~50–200 pg/mL (yorug‘lik va uyqu sikliga bog‘liq)",
        "Oshganda": "Melatoninning yuqori darajasi uyquchanlik va mavsumiy depressiya (qishki vaqt blues) bilan bog‘liq bo‘lishi mumkin; Kechasi me’yoridan ortiq yuqori bo‘lishi uyquga ketishni osonlashtiradi, lekin kunduzi oshib ketishi uyqu bosishiga sabab bo‘ladi",
        "Kamayganda": "Uyqusizlik va sirkad ritm buzilishi (melatonin pastligi oqibatida uyqu sifatining yomonlashuvi); Qarilikda melatonin fiziologik pasayadi",
        "Organizmdagi belgilari": "Yuqori darajada – kun davomida loqaydlik, uyquchanlik, ba’zan depressiv holat; Past darajada – uyquning buzilishi, kechasi uxlay olmaslik, sirkadiy ritmning buzilishi (tunda hushyor yurish va kunduzi o‘ta charchoq)",
        "Qachon tekshirish kerak": "Melatonin darajasi odatda klinik tekshiruvlarda ishlatilmaydi; surunkali uyqu buzilishlari yoki sirkadiy ritmning jiddiy buzilishlarida ilmiy izlanishlar doirasida o‘lchanishi mumkin"
    },
    "Paratireoid gormon (PTH)": {
        "Normasi": "15–65 pg/mL (qonda, kalsiy muvozanatiga bog‘liq ravishda o‘zgaradi)",
        "Oshganda": "Giperparatireoz (qalqonsimon bez oldi bezi o‘smasi yoki giperplaziyasi – qonda PTH ortadi): birlamchi giperparatireozda; Ikkilamchi giperparatireoz (masalan, surunkali buyrak yetishmovchiligida kalsiy past bo‘lsa PTH reaktiv oshadi)",
        "Kamayganda": "Gipoparatireoz (qalqonsimon oldi bezlarining shikastlanishi yoki autoimmun kasalligi tufayli PTH kamayadi); Qonda kalsiy me’yordan yuqori bo‘lganda (masalan, saraton metastazlari sabab hiperkalsiyemiya)",
        "Organizmdagi belgilari": "Yuqori darajada – qonda kalsiy oshishi (hiperkalsiyemiya: chanqoq, ko‘p siyish, buyrak toshlari, qabziyat, suyaklarda og‘riq va sinuvchanlik, asabiylik); Past darajada – qonda kalsiy yetishmovchiligi (gipokalsiyemiya: mushak tutqanoqlari, tirishishlar, uyushish va uvishish hissi, soch va tirnoqlarning mo‘rtlashuvi)",
        "Qachon tekshirish kerak": "Qonda kalsiy darajasi yuqori yoki past chiqqanda, suyaklarning mo‘rtlashuvi yoki buyrak toshlari paydo bo‘lganda (giperparatireozdan shubha), bo‘yin sohasi operatsiyasidan keyin gipoparatireoz belgilari (masalan, mushak spazmlari) kuzatilsa"
    },
    "Gastrin": {
        "Normasi": "Och qoringa <100 pg/mL",
        "Oshganda": "Zollinger-Ellison sindromi (gastrinoma oshqozon osti bezi yoki o‘n ikki barmoq ichak o‘smasi – gastrin ortiqcha ishlab chiqariladi); Pernisioz anemiya (me’da kislotaliligi pasayganda gastrin reflektor oshadi)",
        "Kamayganda": "Me’da sekretor hujayralarining yetishmovchiligi (atrofik gastrit) yoki gipertireoz (moddalar almashinuvi tezligi oshib, gastrin darajasi pasayishi mumkin)",
        "Organizmdagi belgilari": "Yuqori darajada – qorin og‘rig‘i va surunkali ichki yaralar (oshqozon yoki o‘n ikki barmoq ichakda qaytalanuvchi yaralar), diareya va vazn yo‘qotish (gastrinoma belgilaridan); Past darajada – ishtahaning pasayishi, ovqat hazm bo‘lishining sekinlashuvi, me’da kislotaligining kamayishi (ko‘ngil aynishi, B12 vitamini yetishmovchiligi belgilari)",
        "Qachon tekshirish kerak": "Davolash qiyin kechayotgan yoki takrorlanaveradigan me’da va ichak yaralari mavjud bo‘lsa (Zollinger-Ellison sindromidan shubha qilinganda), pernizioz anemiya tashxisi qo‘yishda, me’da kislotaligi past bo‘lgan holatlarda"
    },
    "Sekretin": {
        "Normasi": "Aniq belgilangan normal diapazon yo‘q (sekretin odatda ichakda joyida o‘lchanadi, qon darajasi kam ishlatiladi)",
        "Oshganda": "Duodenum yoki yeyunomda sekretin ajratuvchi neyroendokrin o‘sma (o‘ta nodir holat); Gipersekresiya – oshqozon kislotasining ortiqcha neytrallanishi va pankreatik sekretsiya ortishi",
        "Kamayganda": "Sekretin ajralishining pasayishi (masalan, surunkali pankreatit yoki ichak shikastlanishida) – me’da kislota neutralizatsiyasi sust",
        "Organizmdagi belgilari": "Yuqori darajada – me’da kislotasi tez neytrallanishi tufayli diareya, qorinda og‘riq (oshqozon osti bezi fermentlarining ortiqcha ajralishi ham mumkin); Past darajada – me’da kislotasi to‘liq neytrallanmaydi, o‘n ikki barmoq ichak yaralari rivojlanishi, ovqat hazm bo‘lishining buzilishi (qorinda achishish, ko‘ngil aynishi)",
        "Qachon tekshirish kerak": "Klinik amaliyotda sekretin darajasi deyarli tekshirilmaydi; oshqozon osti bezi faoliyatini baholash uchun sekretin sinovlari qo‘llanadi (masalan, surunkali pankreatitda), yoki nodir gastroenteropankreatik o‘smalardan shubha qilingan hollarda ilmiy tadqiqot sifatida"
    },
    "Xolesistokinin (CCK)": {
        "Normasi": "10–50 pg/mL (och qoringa, ovqatdan so‘ng oshadi)",
        "Oshganda": "Hazm qilish tizimi kasalliklarida (masalan, o‘n ikki barmoq ichak yarasi, pankreatit) kompensator oshishi; Ko‘p yog‘li ovqat iste’mol qilinganda me’yordan ortiq yuqori sezuvchanlik",
        "Kamayganda": "Ovqat hazm qilishning buzilishi (masalan, jig‘ildon qaynashi va hazm sustligi, CCK ajralishi kamayganda o‘t pufagi va pankreatik fermentlar yetarli darajada ajralmaydi)",
        "Organizmdagi belgilari": "Yuqori darajada – yog‘li ovqat iste’molidan keyin qorinda og‘irlik va og‘riq, diareya yoki o‘t pufagi spazmlari; Past darajada – yog‘li ovqatlarga toqatning pasayishi, qorinda dam bo‘lishi, hazm bo‘lishning sustligi (ayniqsa yog‘li taomlardan keyin)",
        "Qachon tekshirish kerak": "Ovqat hazm qilishda muammolar, xususan yog‘li ovqatlarni hazm qilish qiyin bo‘lsa (o‘t pufagi yoki oshqozon osti bezi faoliyatini baholash doirasida). Klinikaning o‘zida CCK darajasini o‘lchash kam qo‘llanadi, asosan ilmiy izlanishlarda"
    },
    "Grelin": {
        "Normasi": "100–300 pg/mL (och qoringa, ovqatlanganda kamayadi)",
        "Oshganda": "Semizlik va anoreksiya nervoza holatlarida grelin darajasi baland bo‘lishi mumkin (ochlik gormoni sifatida organizm ozganda ko‘payadi, ba’zida semizlikda ham grelin supressiyasi buzilishi); Prader-Villi sindromida juda yuqori",
        "Kamayganda": "Metabolik sindrom va semizlikning ba’zi turlarida (grelin past bo‘lsa ham, leptin rezistentligi sabab vazn ortishi davom etadi); Qariyotgan organizmda tabiiy ravishda pasayadi",
        "Organizmdagi belgilari": "Yuqori darajada – doimiy ochlik hissi, ishtahaning kuchayishi, ovqat yeganda ham to‘ymaslik (bu semizlikka hissa qo‘shishi mumkin), anoreksiya nervozada esa yuqori grelin gavdaning ochlik holatini aks ettiradi; Past darajada – ishtahaning susayishi, ovqatlanishni xohlamaslik, metabolik jarayonlarning buzilishi (masalan, semizlikda grelin past bo‘lsa ham vazn tashlash qiyin bo‘lishi)",
        "Qachon tekshirish kerak": "Grelin darajasi asosan ilmiy tadqiqotlarda o‘lchanadi; klinik jihatdan ortiqcha vazn yoki ishtaha bilan bog‘liq kasalliklarni chuqurroq o‘rganishda qo‘llanilishi mumkin (masalan, ishtaha nazoratini tadqiq qilishda)"
    },
    "Leptin": {
        "Normasi": "2–20 ng/mL (tana yog‘i foiziga bog‘liq, semiz odamlarda yuqori, ozg‘in odamlarda pastroq)",
        "Oshganda": "Semizlik (adipotsitlardan leptin ajralishi ortadi); Leptin rezistentligi rivojlanadi, ya’ni leptin yuqori bo‘lsa ham miya to‘yish signalini ololmaydi",
        "Kamayganda": "Anoreksiya va ozg‘inlik (tana yog‘i juda past bo‘lsa, leptin darajasi pasayadi); Bu holatda tuyish signalining yetishmasligi tufayli organizm doimiy ochlik holatida bo‘lishi mumkin",
        "Organizmdagi belgilari": "Yuqori darajada – semizlikka qaramay doimiy ochlik hissi (leptin rezistentligi tufayli), arterial bosimning oshishi (leptin simpatik faollikni oshirishi mumkin); Past darajada – vaznning keskin kamayishi, amenoreya (ayollarda yog‘ yetishmasligidan hayz to‘xtashi), sovuqka nisbatan sezgirlik oshishi",
        "Qachon tekshirish kerak": "Leptin darajasi klinik diagnostikada ko‘p qo‘llanilmaydi; semizlik yoki anoreksiya kabi holatlarning patogenezini tadqiq qilishda yoki klinik sinovlarda o‘lchanishi mumkin"
    },
    "Peptid YY (PYY)": {
        "Normasi": "50–200 pg/mL (ovqatdan keyin oshadi)",
        "Oshganda": "Anoreksiya nervoza (ishtaha yo‘qligida PYY me’yordan yuqori bo‘lishi mumkin, chunki ovqat yemaslik PYY ajralishini kamaytirmaydi); Oshqozonning chetlab o‘tish operatsiyalaridan so‘ng PYY darajasi yuqori (ishtaha pasayishi bilan bog‘liq)",
        "Kamayganda": "Semizlik (PYY ajralishi past bo‘lib, to‘yish signali zaiflashgan bo‘lishi mumkin)",
        "Organizmdagi belgilari": "Yuqori darajada – ishtahaning pasayishi, ozishga moyillik, ovqatdan tez to‘yish; Past darajada – ishtahaning kuchayishi, to‘yish hissining sustligi va natijada ortiqcha ovqatlanish, vazn ortishi",
        "Qachon tekshirish kerak": "Ishtaha bilan bog‘liq ilmiy tadqiqotlarda, semizlikning yoki ovqatlanish buzilishlarining sabab-mexanizmlarini o‘rganishda; klinik amaliyotda oddiy diagnostika uchun PYY darajasi odatda tekshirilmaydi"
    },
    "Motilin": {
        "Normasi": "100–400 pg/mL (och qoringa yuqori, ovqatlanganda pasayadi)",
        "Oshganda": "Ichak harakatining ortishi: masalan, diareyali sindromlar; Ba’zi ichak infeksiyalari motilin ajralishini kuchaytiradi",
        "Kamayganda": "Ovqat hazm qilish motiligini sustligi: masalan, gastroparez (oshqozon bo‘shanishining sekinlashuvi), surunkali qabziyat",
        "Organizmdagi belgilari": "Yuqori darajada – tez-tez ich ketishi, qorinda sanchiq va og‘riq (ichak peristaltikasining kuchayishi); Past darajada – qorinda og‘irlik va dam bo‘lish, ovqat hazm bo‘lishining sekinligi, tez-tez qabziyat",
        "Qachon tekshirish kerak": "Ichak motiliteti buzilishlarida (masalan, sababsiz surunkali diareya yoki sababsiz gastroparezda) tadqiqot maqsadida; klinik diagnostikada motilin darajasi odatda ishlatilmaydi"
    },

    "Angiotenzinogen": {
        "Normasi": "0,5–2,5 mg/L",
        "Oshganda": "Gipertenziya (yurak-qon tomir tizimi kasalliklarida angiotenzinogen ko‘payishi); Jigarning yallig‘lanish va semirishida ham oshishi mumkin",
        "Kamayganda": "Arterial gipotenziya (past qon bosimi); Buyrak yetishmovchiligi (renin-angiotenzin tizimi izdan chiqqanda angiotenzinogen kompensator ravishda kamayishi)",
        "Organizmdagi belgilari": "Yuqori darajada – doimiy yuqori qon bosimi, bosh og‘rig‘i, bosh aylanishi, yurak zo‘riqishi; Past darajada – past qon bosimi, bosh aylanib ketishi, holdan toyish, buyrak funksiyasi buzilishi belgilari",
        "Qachon tekshirish kerak": "Arterial gipertenziya sababini aniqlashda keng qamrovli tadqiqot sifatida; kam hollarda genetik gipertenziya sindromlaridan gumon qilinganda; bu ko‘rsatkich amaliyotda kam o‘lchanadi, asosan ilmiy tekshiruvlarda"
    },
    "IGF-1 (insulin o‘xshash o‘sish faktori)": {
        "Normasi": "100–300 ng/mL (eng yuqori daraja o‘smirlik davrida, yoshi o‘tishi bilan pasayadi)",
        "Oshganda": "Gigantizm (o‘smirlikda o‘sish gormoni oshiq bo‘lsa IGF-1 yuqori); Akromegaliya (kattalarda GH oshishi bilan IGF-1 ham oshadi); Ba’zi o‘sma kasalliklarida (IGF-1 ning autokrin oshishi)",
        "Kamayganda": "GH yetishmovchiligi (past IGF-1 – bolalarda o‘sish sustligi); Qariyotgan organizm (yosh o‘tishi bilan kamayadi); Surunkali kasallik va ishtaha yo‘qligida (nutritiv yetishmovchilikda)",
        "Organizmdagi belgilari": "Yuqori darajada – bolalarda haddan tashqari bo‘y o‘sishi va katta tana o‘lchamlari (gigantizm), kattalarda qo‘l-oyoq va yuz suyaklarining kattalashishi, jag‘ chiqishi (akromegaliya), qo‘lning uvishishi, qandli diabetga moyillik; Past darajada – bolalarda bo‘y o‘smasligi, jismoniy rivojlanishning sekinligi, kattalarda mushaklarning zaiflashishi, suyak zichligining pasayishi va charchoq",
        "Qachon tekshirish kerak": "Bolalarda o‘sish sustligi yoki mittilikdan shubha qilinganda (GH yetishmovchiligini tekshirish uchun), kattalarda akromegaliya belgilari kuzatilganda, shuningdek, o‘sish gormoniga bog‘liq davolash jarayonini kuzatishda"
    },
    "Hepcidin": {
        "Normasi": "10–100 ng/mL",
        "Oshganda": "Surunkali yallig‘lanish kasalliklarida va temir tanqisligi anemiyasida (hepcidin darajasi patologik yuqori bo‘lishi mumkin, bu temirning o‘zlashtirilishini kamaytiradi) – ya’ni autoimmun va infeksion kasalliklarda anemiya; Gemokromatoz davolashida sun’iy oshirilsa",
        "Kamayganda": "Nasliy gemokromatoz (hepcidin past, temir ortiqcha to‘planadi); Surunkali gepatit va jigar yetishmovchiligi (hepcidin ishlab chiqarilishi pasayadi) – bu holda temir ortiqchaligi kuzatiladi",
        "Organizmdagi belgilari": "Yuqori darajada – qon zardobida temir past bo‘lib, temir tanqisligi anemiyasi alomatlari: holsizlik, bosh aylanishi, terining oqarganligi, brittle (mo‘rt) tirnoqlar; Past darajada – qonda va to‘qimalarda temir ortishi: terining qorayib pigmente bo‘lishi (bronza rang), bo‘g‘im og‘riqlari, jigar kattalashishi va disfunksiyasi, qandli diabet (\"bronza diabet\")",
        "Qachon tekshirish kerak": "Temir moddasining almashinuvi buzilishi shubhasida: sababi tushunarsiz temir tanqisligi anemiyasi yoki gemokromatoz (temirning ortiqcha to‘planishi) aniqlanganda, ushbu kasalliklarning tasdiqi uchun hepcidin darajasini o‘lchash ilmiy-amaliy jihatdan foydali bo‘lishi mumkin"
    },
    "Adiponektin": {
        "Normasi": "4–30 µg/mL (erkaklarda biroz pastroq, ayollarda yuqoriroq me’yorga moyil)",
        "Oshganda": "Surunkali kasalliklar va ba’zi anemiya turlarida (masalan, \"ochiq qizil\" anemiya – ehtimol pernisi oz anemiya nazarda tutilgan) adiponektin darajasi oshishi mumkin; Shuningdek, vazn tashlaganda va jismoniy faollik oshganda adiponektin ortadi",
        "Kamayganda": "Semizlikda va 2-tip qandli diabetda adiponektin darajasi past (insulin qarshiligi bilan bog‘liq); Metabolik sindrom komponentlarida adiponektin kamayadi",
        "Organizmdagi belgilari": "Yuqori darajada – ko‘pincha asosiy surunkali kasallik belgilariga hamroh bo‘ladi (masalan, yallig‘lanish kasalliklarida); metabolik jihatdan, insulin sezuvchanligi yaxshiroq bo‘lishi mumkin; Past darajada – insulin rezistentligi va metabolik sindrom belgilariga hissa qo‘shadi (ortiqcha vazn, yuqori qon bosimi, qandli diabet), yog‘ to‘qimalarining ortiqligi",
        "Qachon tekshirish kerak": "Asosan ilmiy tadqiqotlarda semizlik va metabolik sindromni o‘rganishda; oddiy klinik amaliyotda adiponektin darajasi odatda o‘lchanmaydi, chunki metabolik salomatlikni bilvosita boshqa ko‘rsatkichlar bilan baholash mumkin"
    },
    "Rezistin": {
        "Normasi": "5–20 ng/mL",
        "Oshganda": "Semizlik va 2-tip qandli diabet (rezistin darajasi yuqori bo‘lib, insulin qarshiligini kuchaytiradi); Metabolik sindrom",
        "Kamayganda": "Ozg‘inlik, kaloriyali cheklangan parhez (tana yog‘i kam bo‘lganda); Insulin sezuvchanlik oshgan holatlar",
        "Organizmdagi belgilari": "Yuqori darajada – qonda glyukoza yuqori (insulin yetarli ta’sir qilmagani uchun), qorin atrofida yog‘ to‘planishi, qon yog‘lari miqdori oshishi (dislipidemiya); Past darajada – insulin ta’siri yaxshiroq, metabolizm tezligi nisbatan me’yorda yoki yuqori, ortiqcha vazn yo‘qligi",
        "Qachon tekshirish kerak": "Rezistin ham odatda klinik diagnostikada o‘lchanmaydi; metabolik sindrom va diabet patogenezini o‘rganishda ilmiy jihatdan ahamiyatga ega"
    },
    "Atrial natriyuretik peptid (ANP)": {
        "Normasi": "20–77 pg/mL",
        "Oshganda": "Yurak yetishmovchiligi (yurak bo‘lmachalarida cho‘zilish – ANP ko‘payishi), surunkali yurak-qon tomir yetishmovchiligi va gipervolemiya holatlari",
        "Kamayganda": "Qon hajmining kamayishi va past qon bosimi (gipovolemiya); Og‘ir buyrak yetishmovchiligi (ANP sekretsiyasi buzilishi mumkin)",
        "Organizmdagi belgilari": "Yuqori darajada – tanada suyuqlik to‘planishi (qorin va oyoqlarda shishlar), tez charchash, nafas qisishi (yurak yetishmovchiligi alomatlari); Past darajada – past qon bosimi, bosh aylanishi, suyuqlikning tanqisligi alomatlari (og‘iz qurishi, tez charchash)",
        "Qachon tekshirish kerak": "Yurak yetishmovchiligini aniqlash va og‘irlik darajasini baholash uchun (ANP va unga o‘xshash BNP klinikada ishlatiladi); Shuningdek, o‘tkir yurak sindromlari differensial diagnostikasida"
    },
    "Beyn natriyuretik peptid (BNP)": {
        "Normasi": "<100 pg/mL",
        "Oshganda": "Yurak yetishmovchiligi (BNP darajasi yurak qorinchalari kengayganda ortadi); O‘tkir yurak infarktida va chap qorinch yetishmovchiligida ham ko‘tariladi",
        "Kamayganda": "Normal holat yoki muvaffaqiyatli davolangan yurak yetishmovchiligi; Patologik past holati ahamiyatli emas (odatda norma sifatida qabul qilinadi)",
        "Organizmdagi belgilari": "Yuqori darajada – nafas qisishi, to‘sh osti og‘riqlari, oyoqlarda shish (yurak yetishmovchiligi belgilari); Past darajada – belgilari yo‘q (yurak faoliyati me’yorda bo‘lishi mumkin)",
        "Qachon tekshirish kerak": "Yurak yetishmovchiligini diagnostika qilish va kuzatishda (BNP darajasi kasallik og‘irligini ko‘rsatadi), nafas qisishi shikoyati bo‘lgan bemorda sabab yurakmi yoki o‘pkami ekanini ajratishda"
    },
    "Eritropoetin (EPO)": {
        "Normasi": "Erkaklarda: 4,3–29 mIU/mL; Ayollarda: 3,7–26 mIU/mL",
        "Oshganda": "Surunkali gipoksiya (masalan, baland tog‘da uzoq vaqt yashash yoki surunkali o‘pka kasalliklari – organizm kislorod yetishmovchiligiga javoban EPO oshiradi); Ikkilamchi policitemiya (masalan, buyrak kistalari yoki o‘smasi EPO ni ko‘p ishlab chiqarishi); Birlamchi policitemiya vera (qon yaratuvchi tizim kasalligi) – bunda EPO odatda past yoki normal bo‘lsa-da, ayrim hollarda EPO me’yordan biroz yuqori bo‘lishi mumkin",
        "Kamayganda": "Surunkali buyrak yetishmovchiligi (buyraklar EPO ni kam ishlab chiqaradi – natijada kamqonlik); Ayrim revmatik va surunkali kasalliklar kamqonligida (EPO ishlab chiqarilishi yetarlicha emas)",
        "Organizmdagi belgilari": "Yuqori darajada – qonni quyuqlashishi (eritrositoz): bosh og‘rig‘i, bosh aylanishi, qon bosimi oshishi, terining qizarishi; Past darajada – kamqonlik alomatlari: holsizlik, bosh aylanishi, teri oqargan, nafas qisishi jismoniy faollikda",
        "Qachon tekshirish kerak": "Kamqonlikning sababi aniqlanmaganda (ayniqsa buyrak kasalligiga shubha bo‘lsa), eritrositoz (eritrotsitlar va gemoglobin miqdori yuqori) kuzatilganda policitemiya turini aniqlash uchun (birlamchi yoki ikkilamchi) EPO darajasini tekshirish zarur bo‘lishi mumkin"
    },
    "Renin": {
        "Normasi": "Yotgan holatda: 0,2–1,6 ng/mL/soat; Tik turganda: 1,0–6,5 ng/mL/soat",
        "Oshganda": "Renovaskulyar gipertenziya (buyrak arteriyasi torayishi – renin sekretsiyasi oshadi); Gipotenziya (qon bosimi past bo‘lsa renin reflektor oshadi); Surunkali tuz tanqisligi; 1-tip qandli diabet nefropatiyasi (buyrak qon oqimi pasayganda renin ko‘payishi mumkin)",
        "Kamayganda": "Birlamchi giperalosteronizm (Conn sindromi – aldosteron oshib ketib renin bosiladi); Essensial gipertenziyaning ba’zi shakllari (renin-past gipertenziya); Qon hajmining ortishi (gipervolemiya, yurak yetishmovchiligi)",
        "Organizmdagi belgilari": "Yuqori darajada – qon bosimining oshib-pasayib turishi, ba’zida ortostatik bosh aylanishi; Ko‘p terlash va chanqoqlik (renin-angiotenzin tizimi faolligiga bog‘liq alomatlar); Past darajada – doimiy yuqori qon bosimi, past kaliy (birlamchi aldosteronizm belgilariga hamroh), ba’zan hech qanday alomat sezilmasligi ham mumkin",
        "Qachon tekshirish kerak": "Arterial qon bosimi juda yuqori bo‘lib, sababi aniqlanmasa (gormoniy gidertenziya turlarini farqlash uchun), gipokalemiya (qonda kaliy past) bilan birga yuqori qon bosimi kuzatilsa (aldosteron/renin nisbatini baholash uchun), shuningdek, buyrak kasalliklariga shubha bo‘lsa renin darajasini tekshirish tavsiya etiladi"
    },
    "Timulin": {
        "Normasi": "Aniq doimiy norma mavjud emas, yosh o‘tishi bilan tabiiy ravishda pasayadi",
        "Oshganda": "Timus bezi o‘smalari yoki giperplaziyasida timulin darajasi ortishi mumkin, bu esa autoimmun reaksiyalar xavfini oshiradi",
        "Kamayganda": "Timusning involyusiyasi (o‘smirlikdan keyin timus kichrayadi) yoki immun tanqislik holatlari (timus faoliyati past) – natijada immunitet susayishi",
        "Organizmdagi belgilari": "Yuqori darajada – autoimmun kasalliklarga moyillik ortishi, immun tizimining haddan tashqari faolligi (masalan, myasthenia gravis timoma bilan bog‘liq); Past darajada – tez-tez infeksiyalar bilan kasallanish, organizmning infeksiyalarga qarshi zaifligi, vaksinalarga sust immun javob",
        "Qachon tekshirish kerak": "Rutin tekshiruvlarda timulin o‘lchanmaydi; immunitet jiddiy susaygan bemorlarda (masalan, davomli infeksiyalar, kombine immun tanqislikda) yoki timus o‘smalariga shubha qilinganda ilmiy izlanish doirasida o‘lchanishi mumkin"
    },
    "Timopoetin": {
        "Normasi": "Aniq norma belgilanmagan (timopoetin darajasi yoshga qarab kamayadi, kattalarda juda past)",
        "Oshganda": "Timus bezining o‘smasida (timomada) yoki immun tizimining ayrim buzilishlarida oshishi mumkin – bu autoimmun jarayonlar xavfini oshirishi mumkin",
        "Kamayganda": "Yoshi o‘tishi bilan tabiiy ravishda pasayadi; Gipopituitarizm yoki og‘ir immun tanqislik holatlarida ham timopoetin darajasi past bo‘ladi",
        "Organizmdagi belgilari": "Yuqori darajada – autoimmun kasalliklar (masalan, timus o‘smasi bilan bog‘liq Myastenia Gravis) belgilari paydo bo‘lishi mumkin; Past darajada – immunitetning pasayishi, tez-tez infeksiyalarga chalinish, bolalikda timopoetin past bo‘lsa, limfotsitlar yetilishi buzilishi tufayli og‘ir infeksiyalar",
        "Qachon tekshirish kerak": "Timopoetin darajasi amalda klinik laboratoriyada o‘lchanmaydi; timus faoliyatini tadqiq qilishda va immun tizimining chuqur buzilishlarida ilmiy-tadqiqot maqsadlarida o‘lchanishi mumkin"
    },
    "Interleykinlar (IL-1, IL-6, IL-10)": {
        "Normasi": "IL-1: <5 pg/mL; IL-6: <1,5 pg/mL; IL-10: 2–20 pg/mL",
        "Oshganda": "Yallig‘lanish va infeksiya kasalliklarida (masalan, revmatoid artrit, sepsis) IL-1 va IL-6 darajalari oshadi; Autoimmun kasalliklarda (IL-6 oshishi); Surunkali infeksiyalarda; IL-10 ba’zan ba’zi limfoma va virusli infeksiyalarda oshishi mumkin",
        "Kamayganda": "Yallig‘lanish javobining susayishi (masalan, immunosupressiv davolash fonida); Og‘ir immun tanqislikda (interleykin ishlab chiqaruvchi hujayralar faoliyati pasaysa)",
        "Organizmdagi belgilari": "Yuqori darajada – isitma, qaltirash, ishtahaning yo‘qolishi, og‘riq va shish (IL-1 va IL-6 yallig‘lanish mediatorlari); Surunkali yallig‘lanishda – ozib ketish, kamqonlik; Past darajada – infeksiyalarga nisbatan sust reaksiya, yallig‘lanish belgisining uncha bilinmasligi, lekin bu holat infeksiya xavfini oshiradi",
        "Qachon tekshirish kerak": "Surunkali yallig‘lanishli yoki autoimmun kasalliklardan shubhalanganda diagnostik biokimyoviy marker sifatida (masalan, IL-6 ni CRP bilan birga baholash); sepsisda prognostik ko‘rsatkich sifatida IL-6; klinik amaliyotda interleykinlar cheklangan hollarda o‘lchanadi, asosan ilmiy tadqiqot va maxsus klinik vaziyatlarda"
    },
    "Chorionik gonadotropin (hCG)": {
        "Normasi": "Homilador bo‘lmagan ayollarda: <5 mIU/mL; Homiladorlik 3-4-haftasida: ~5–425 mIU/mL; 8-12-haftada: 25 700–288 000 mIU/mL (cho‘qqi daraja)",
        "Oshganda": "Ko‘p homilalik (egizaklar) homiladorlikda hCG me’yordan balandroq bo‘lishi mumkin; Xorial rak yoki xorionepitelioma (yo‘ldosh to‘qimasining o‘smalari) hCG ni juda ko‘p ajratadi; Ba’zi tuxumdon kistalari va o‘sma jarayonlar hCG darajasini oshirishi mumkin",
        "Kamayganda": "Homiladorlikning tug‘ma xavfi ortishi (masalan, homila rivojlanishi sekinlashganda yoki tushish xavfi bo‘lganda hCG o‘sishi me’yordan sekin); Bachadondan tashqari homiladorlikda hCG darajasi kutilganidan past bo‘ladi",
        "Organizmdagi belgilari": "Yuqori darajada – homiladorlik belgilarining kuchli namoyon bo‘lishi (toxikoz – ko‘ngil aynishi, qusish kuchli), homiladorlik bo‘lmasa: bachadondan qon ketishi, qorin og‘rig‘i (xorionepitelioma belgisi bo‘lishi mumkin); Past darajada – homiladorlik davomida ko‘ngil aynish kabi belgilar kam bo‘lishi, homila harakatlarining sustligi, homila o‘sishi sekin (potentsial xavf belgisi)",
        "Qachon tekshirish kerak": "Homiladorlikni erta aniqlash (test sifatida), normal homiladorlik rivojini kuzatish (birinchi trimestrda hCG dinamikasini baholash), bachadondan tashqari homiladorlikdan shubhalanganda, homiladorlik paytida qon ketishi yoki tushish xavfi bo‘lganda; shuningdek, trofoblast o‘smalarini (masalan, xorionepitelioma) diagnostika va kuzatishda"
    },
    "Platsentada ishlab chiqariladigan laktogen gormon (hPL)": {
        "Normasi": "Homiladorlikning 24–28-haftasida eng yuqori darajaga chiqadi (aniq miqdori haftaga va homila soniga bog‘liq, taxminan maksimal 5–7 µg/mL atrofida)",
        "Oshganda": "Ko‘p homilali homiladorlikda (egizaklarda) hPL darajasi bir fetusega nisbatan balandroq; Yo‘ldosh (platsenta) juda katta bo‘lganda yoki platsentaning qalinlashuvi",
        "Kamayganda": "Platsentar yetishmovchilik – yo‘ldosh yaxshi rivojlanmaganda yoki zararlanganda hPL ishlab chiqarilishi past bo‘ladi; Bu hol homila o‘sishining sustlashishi bilan bog‘liq bo‘lishi mumkin",
        "Organizmdagi belgilari": "Yuqori darajada – onaning organizmida insulin rezistentligi kuchayishi (homiladorlik diabeti rivojlanishi mumkin), ko‘krak bezlari erta kattalashishi va sutga tayyorgarlik; Past darajada – homilaning o‘sish sekinligi, homiladorlik davrida ona vazn ololmasligi yoki homila harakatlari me’yordan kamligi",
        "Qachon tekshirish kerak": "hPL odatda rutinda o‘lchanmaydi; agar homila o‘sishdan orqada qolayotgan bo‘lsa yoki yo‘ldosh yetarli ishlamayotganidan shubha qilinsa, boshqa tekshiruvlar qatorida platsentar gormonlar darajasini baholash uchun o‘lchanishi mumkin"
    },
    "Progesteron (homiladorlik davri)": {
        "Normasi": "Homiladorlik 1-trimestri: 11–44 ng/mL; 3-trimestri oxirida: 100–300 ng/mL (ayollarda homiladorlik davomida keskin oshadi)",
        "Oshganda": "Homiladorlikda yuqori – normal holat (ayniqsa, egizak homiladorlikda balandroq bo‘lishi mumkin); Homiladorlikdan tashqari – progesteronli dori qabulida yoki kamdan kam hollarda buyrak usti bezining steroid gormon o‘smasida",
        "Kamayganda": "Homiladorlik paytida platsentarning yetarli ishlamasligi (progesteron past bo‘lsa, homila tushish xavfi); Homiladorlikdan tashqari – luteal faza yetishmovchiligi (natijada bepushtlik yoki erta tushish)",
        "Organizmdagi belgilari": "Yuqori darajada – homiladorlik belgilarining kuchayishi (uyquchanlik, ko‘krak sezuvchanligi, ba’zan engil bosh aylanishi); Past darajada – homiladorlikning erta bosqichida qorinda tortish yoki og‘riq, qonli ajralmalar (tushish xatarining belgisi), odatdagi hayz oldi sindromining og‘irlashishi yoki homilador bo‘lmasa hayz oldidan dog‘lanish",
        "Qachon tekshirish kerak": "Erta homiladorlikda, agar homila tushish xavfi yoki bachadondan tashqari homiladorlikdan shubha bo‘lsa (progesteron darajasi past bo‘lishi mumkin); bepushtlikni tekshirishda luteal faza yetukligini baholash uchun (ayniqsa, takroriy homila tushishlar bo‘lsa) progesteron darajasini o‘lchash foydali"
    },

