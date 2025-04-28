from telegram import Update, ReplyKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters import os

Asosiy menyu

def get_main_menu(): main_menu_keyboard = [ ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"], ["Bioximiya haqida", "Klinika haqida"], ["IXLA va IFA tekshiruv farqi"], ["Biz bilan bog'lanish", "Admin bilan bog'lanish"], ["Tahlil natijalarini olish", "Taklif va shikoyatlar"], ["Kitob (Analizlar haqida to‘liq ma'lumot)"], ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilmoqda?"] ] return ReplyKeyboardMarkup(keyboard=main_menu_keyboard, resize_keyboard=True)

Tahlillar haqida guruhlar

def get_analysis_menu(): analysis_keyboard = [ ["Gormonlar", "TORCH Paneli"], ["Onkomarkerlar", "Vitaminlar va Anemiya"], ["Kardiomarkerlar", "Koagulyatsiya markerlari"], ["Suyak metabolizmi", "Jigar fibrozi"], ["Buyrak funksiyasi", "Immunoglobulinlar"], ["Autoimmun panel", "Yuqumli kasalliklar"], ["Allergenlar", "Dori vositalarini nazorati"], ["Umumiy qon tahlillari", "Siydik tahlillari"], ["⬅️ Orqaga"] ] return ReplyKeyboardMarkup(keyboard=analysis_keyboard, resize_keyboard=True)

/start komandasi

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "\U0001F9EC Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n" "\U0001F52C Zamonaviy IXLA texnologiyasi asosida:\n" "- Gormonlar\n- TORCH Paneli\n- Onkomarkerlar\n- Bioximik tahlillar\n- Umumiy qon va siydik tahlillarini sifatli va tezkor amalga oshiramiz.\n\n" "\U0001F4CD Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n" "\U0001F4DE Telefon: +998 90 741 72 22\n" "\U0001F4F7 Instagram: @akmal.jon7222\n\n" "\u2705 Biz uchun daromaddan ko'ra to'g'ri natija va bemor ishonchi muhim!\n\u2705 Ishonchli diagnostika - sog'ligingiz kafolati!", reply_markup=get_main_menu() )

Menyu boshqarish

async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text

if text == "Tahlillar haqida ma'lumot":
    await update.message.reply_text("Quyidagi tahlil guruhlaridan birini tanlang:", reply_markup=get_analysis_menu())
elif text == "⬅️ Orqaga":
    await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
elif text == "Qon topshirish qoidalari":
    await update.message.reply_text("Qon topshirish uchun:\n- 8-12 soat och qoling.\n- Ertalab 7:00-10:00 oralig'ida topshirish tavsiya etiladi.\n- Suv ichish mumkin.")
elif text == "Bioximiya haqida":
    await update.message.reply_text("Bioximiya tahlillariga: jigar, buyrak, yurak va boshqa organ ko'rsatkichlari kiradi.")
elif text == "Klinika haqida":
    await update.message.reply_text("Klinik tahlillar: umumiy qon analizi, siydik analizi va boshqa testlar.")
elif text == "IXLA va IFA tekshiruv farqi":
    await update.message.reply_text("IXLA zamonaviy, tezkor va aniq texnologiya. IFA esa eski metod.")
elif text == "Biz bilan bog'lanish":
    await update.message.reply_text("\ud83d\udccd Kosonsoy tumani, Kattalar poliklinikasi yonida\n\ud83d\udcde +998 90 741 72 22\n\ud83d\udcf8 Instagram: @akmal.jon7222\n✉️ Email: akmaljon.1990k.ru@gmail.com")
elif text == "Admin bilan bog'lanish":
    await update.message.reply_text("Admin bilan bog'lanish: @akmaljon_lab")
elif text == "Tahlil natijalarini olish":
    await update.message.reply_text("Tahlil natijasi olish uchun ID raqamingizni kiriting.")
elif text == "Taklif va shikoyatlar":
    await update.message.reply_text("Taklif yoki shikoyatlaringizni yozing, adminga yuboriladi.")
elif text == "Kitob (Analizlar haqida to‘liq ma'lumot)":
    await update.message.reply_text("Kitob haqida ma'lumot olish uchun 'Kitob' deb yozing.\nNarxi: 45 000 so'm.")
elif text == "Botga foydalanuvchi qo‘shish":
    await update.message.reply_text("Do'stlaringizga ham botni tavsiya qiling!")
elif text == "Sizni nima bezovta qilmoqda?":
    await update.message.reply_text("Bezovta qilayotgan narsani yozing. Maslahat beramiz.")
else:
    await update.message.reply_text("Iltimos, menyudan kerakli tugmani tanlang.")

Main funksiya

def main(): token = os.getenv("TOKEN") if not token: raise RuntimeError("Bot token topilmadi. .env faylga TOKEN kiriting.")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
app.run_polling()

if name == "main": main()

