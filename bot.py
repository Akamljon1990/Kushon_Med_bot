Importlar

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters import os

Asosiy menyu

main_menu_keyboard = [ ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"], ["Bioximiya haqida", "Klinika haqida"], ["IXLA va IFA tekshiruv farqi"], ["Biz bilan bog'lanish", "Admin bilan bog'lanish"], ["Tahlil natijalarini olish", "Taklif va shikoyatlar"], ["Kitob (Analizlar haqida to‘liq ma'lumot)"], ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilmoqda?"] ] main_menu = ReplyKeyboardMarkup( keyboard=main_menu_keyboard, resize_keyboard=True )

Tahlillar haqida tahlil guruhlari menyusi

tahlillar_buttons = [ ["Gormonlar", "TORCH Paneli"], ["Onkomarkerlar", "Vitaminlar va Anemiya"], ["Kardiomarkerlar", "Koagulyatsiya markerlari"], ["Suyak metabolizmi", "Jigar fibrozi"], ["Buyrak funksiyasi", "Immunoglobulinlar"], ["Autoimmun panel", "Yuqumli kasalliklar"], ["Allergenlar", "Dori vositalarini nazorati"], ["Umumiy qon tahlillari", "Siydik tahlillari"] ] tahlillar_menu = ReplyKeyboardMarkup( keyboard=tahlillar_buttons, resize_keyboard=True )

/start komandasi

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n" "🔬 Zamonaviy IXLA texnologiyasi asosida:\n" "- Gormonlar\n- TORCH Paneli\n- Onkomarkerlar\n- Bioximik tahlillar\n- Umumiy qon va siydik tahlillarini sifatli amalga oshiramiz.\n\n" "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n" "📞 Telefon: +998 90 741 72 22\n" "📸 Instagram: @akmal.jon7222\n\n" "✅ Biz uchun daromaddan ko'ra to'g'ri natija va bemor ishonchi muhim!\n\n" "✅ Ishonchli diagnostika - sog'ligingiz kafolati!", reply_markup=main_menu )

Menyu tugmalarini boshqarish

async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text

if text == "Tahlillar haqida ma'lumot":
    await update.message.reply_text("Tahlil guruhlaridan birini tanlang:", reply_markup=tahlillar_menu)
elif text == "Qon topshirish qoidalari":
    await update.message.reply_text("Qon topshirish uchun:\n- 8-12 soat och qoling.\n- Ertalab 7:00-10:00 oralig'ida topshirish tavsiya etiladi.\n- Suv ichish mumkin.")
elif text == "Bioximiya haqida":
    await update.message.reply_text("Bioximiya tahlillari: jigar, buyrak, yurak va boshqa organlar ko'rsatkichlari.")
elif text == "Klinika haqida":
    await update.message.reply_text("Klinik tahlillar: umumiy qon va siydik tahlillari.")
elif text == "IXLA va IFA tekshiruv farqi":
    await update.message.reply_text("IXLA - zamonaviy va aniqligi yuqori texnologiya.\nIFA - eskiroq metod.")
elif text == "Biz bilan bog'lanish":
    await update.message.reply_text("\ud83d\udccd Kosonsoy tumani, Kattalar poliklinikasi yonida\n\ud83d\udcde +998 90 741 72 22\n\ud83d\udcf8 Instagram: @akmal.jon7222\n✉️ Email: akmaljon.1990k.ru@gmail.com")
elif text == "Admin bilan bog'lanish":
    await update.message.reply_text("Admin uchun @akmaljon_lab bilan bog'laning.")
elif text == "Tahlil natijalarini olish":
    await update.message.reply_text("Natija olish uchun ID raqamingizni yuboring.")
elif text == "Taklif va shikoyatlar":
    await update.message.reply_text("Taklif yoki shikoyatlaringizni yozing.")
elif text == "Kitob (Analizlar haqida to‘liq ma'lumot)":
    await update.message.reply_text("Kitob haqida ma'lumot olish uchun 'Kitob' deb yozing.\nNarxi: 45 000 so'm.")
elif text == "Botga foydalanuvchi qo‘shish":
    await update.message.reply_text("Do'stlaringizga ham botni tavsiya qiling!")
elif text == "Sizni nima bezovta qilmoqda?":
    await update.message.reply_text("Sizni bezovta qilayotgan narsani yozing, maslahat beramiz.")
else:
    await update.message.reply_text("Iltimos, menyudan kerakli bo'limni tanlang.")

Main

def main(): token = os.getenv("TOKEN") if not token: raise RuntimeError("Bot token topilmadi. .env faylga TOKEN kiriting.")

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))

app.run_polling()

if name == "main": main()

