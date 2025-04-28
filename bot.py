from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

Asosiy menyu

def get_main_menu(): main_menu_keyboard = [ ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"], ["Bioximiya haqida", "Klinika haqida"], ["IXLA va IFA tekshiruv farqi"], ["Biz bilan bog'lanish", "Admin bilan bog'lanish"], ["Tahlil natijalarini olish", "Taklif va shikoyatlar"], ["Kitob (Analizlar haqida to‘liq ma'lumot)"], ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilmoqda?"] ] return ReplyKeyboardMarkup(keyboard=main_menu_keyboard, resize_keyboard=True)

Tahlillar haqida Inline menyu

def get_tests_menu(): tests_menu_keyboard = [ [InlineKeyboardButton("Gormonlar", callback_data="Gormonlar"), InlineKeyboardButton("TORCH Paneli", callback_data="TORCH Paneli")], [InlineKeyboardButton("Onkomarkerlar", callback_data="Onkomarkerlar"), InlineKeyboardButton("Vitaminlar va Anemiya", callback_data="Vitaminlar va Anemiya")], [InlineKeyboardButton("Kardiomarkerlar", callback_data="Kardiomarkerlar"), InlineKeyboardButton("Koagulyatsiya markerlari", callback_data="Koagulyatsiya markerlari")], [InlineKeyboardButton("Suyak metabolizmi", callback_data="Suyak metabolizmi"), InlineKeyboardButton("Jigar fibrozi", callback_data="Jigar fibrozi")], [InlineKeyboardButton("Buyrak funksiyasi", callback_data="Buyrak funksiyasi"), InlineKeyboardButton("Immunoglobulinlar", callback_data="Immunoglobulinlar")], [InlineKeyboardButton("Autoimmun panel", callback_data="Autoimmun panel"), InlineKeyboardButton("Yuqumli kasalliklar", callback_data="Yuqumli kasalliklar")], [InlineKeyboardButton("Allergenlar", callback_data="Allergenlar"), InlineKeyboardButton("Dori vositalarini nazorati", callback_data="Dori vositalarini nazorati")], [InlineKeyboardButton("Umumiy qon tahlillari", callback_data="Umumiy qon tahlillari"), InlineKeyboardButton("Siydik tahlillari", callback_data="Siydik tahlillari")] ] return InlineKeyboardMarkup(tests_menu_keyboard)

/start komandasi

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "\U0001F9EC Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n" "\U0001F52C Biz zamonaviy IXLA texnologiyasi asosida:\n" "– Gormonlar\n– TORCH Paneli\n– Onkomarkerlar\n– Bioximik tahlillar\n– Umumiy qon va siydik tahlillarini sifatli va tezkor amalga oshiramiz.\n\n" "\U0001F4CD Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n" "\U0001F4DE Telefon: +998 90 741 72 22\n" "\U0001F4F8 Instagram: @akmal.jon7222\n\n" "\u2705 Biz uchun daromaddan ko'ra to'g'ri natija va bemor ishonchi muhim!\n\n" "\u2705 Ishonchli diagnostika – sog'ligingiz kafolati!", reply_markup=get_main_menu() )

Menyu tugmalarini boshqarish

async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text

if text == "Tahlillar haqida ma'lumot":
    await update.message.reply_text("Kerakli tahlil guruhini tanlang:", reply_markup=get_tests_menu())
elif text == "Qon topshirish qoidalari":
    await update.message.reply_text("Qon topshirish uchun:\n- 8-12 soat och qoling.\n- Ertalab 7:00-10:00 oralig'ida topshiring.\n- Suv ichish mumkin.")
elif text == "Bioximiya haqida":
    await update.message.reply_text("Bioximiya tahlillariga: jigar, buyrak, yurak, suyak va boshqa organ ko'rsatkichlari kiradi.")
elif text == "Klinika haqida":
    await update.message.reply_text("Klinik tahlillar: umumiy qon analizi, siydik analizi va boshqa klinik testlarni o'z ichiga oladi.")
elif text == "IXLA va IFA tekshiruv farqi":
    await update.message.reply_text("IXLA - zamonaviy va tezkor texnologiya.\nIFA - klassik metod, natijasi sekin va aniqligi pastroq.")
elif text == "Biz bilan bog'lanish":
    await update.message.reply_text("Biz bilan bog'lanish:\n\U0001F4CD Kosonsoy tumani, Kattalar poliklinikasi yonida\n\U0001F4DE +998 90 741 72 22\n\U0001F4F8 Instagram: @akmal.jon7222\n\u2709️ Email: akmaljon.1990k.ru@gmail.com")
elif text == "Admin bilan bog'lanish":
    await update.message.reply_text("Admin uchun murojaat: @akmaljon_lab")
elif text == "Tahlil natijalarini olish":
    await update.message.reply_text("Tahlil natijasi uchun ID raqamingizni kiriting.")
elif text == "Taklif va shikoyatlar":
    await update.message.reply_text("Taklif yoki shikoyatingizni yozing. Xabaringiz adminga yuboriladi.")
elif text == "Kitob (Analizlar haqida to‘liq ma'lumot)":
    await update.message.reply_text("Testlar haqida to'liq ma'lumot olish uchun 'Kitob' so'zini adminga yuboring.\nNarxi: 45 000 so'm. ❗️ Pullik xizmat!")
elif text == "Botga foydalanuvchi qo‘shish":
    await update.message.reply_text("Bot foydali bo'lsa, do'stlaringizga ham tavsiya qiling!")
elif text == "Sizni nima bezovta qilmoqda?":
    await update.message.reply_text("Bizga yozing! Sizni qiynayotgan muammo haqida maslahat beramiz.")
else:
    await update.message.reply_text("Iltimos, menyudan kerakli bo'limni tanlang.")

Callback uchun (hozircha testlar tugmalarini bosganda shunchaki nomini chiqaramiz)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() await query.edit_message_text(f"Siz tanlagan test guruhi: {query.data}")

Main

def main(): token = os.getenv("TOKEN") if not token: raise RuntimeError("Bot token topilmadi. Iltimos .env faylga TOKEN yozing.")

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()

if name == "main": main()

