from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- Gormon va TORCH ma'lumotlari ---
hormone_info = {
    "TSH": "📊 Norma: 0.27–4.2 mIU/L\n🔻 Kamaysa: gipertiroidizm\n🔺 Oshganda: gipotiroidizm",
    # ... (yana 49 gormon haqidagi qisqargan ma'lumotlar joylashadi)
}

torch_info = {
    "Toxoplasma IgM": "📊 Norma: Manfiy (<0.9 IU/mL)\n🔻 Kam: infeksiya yo‘q\n🔺 Ijobiy: yaqinda yuqqan",
    # ... (yana 19 ta TORCH testi haqidagi qisqargan ma'lumotlar joylashadi)
}

# --- Klaviatura funksiyalari ---
def get_main_menu():
    keyboard = [
        ["📋 Tahlillar", "📞 Admin bilan bog‘lanish"],
        ["ℹ️ Biz haqimizda", "📊 Tahlil natijalari"],
        ["✍️ Taklif va shikoyatlar", "📚 Kitob haqida"],
        ["🚀 Start"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_analysis_menu():
    keyboard = [
        ["🧪 Gormonlar", "🧫 TORCH"] ,
        ["💉 Onkomarkerlar", "❤️ Kardiomarkerlar"],
        ["🩸 Umumiy qon", "🚽 Siydik tahlili"],
        ["🧬 Autoimmun", "🧷 Immunoglobulinlar"],
        ["💊 Vitaminlar", "🧪 Biokimyo"],
        ["🦴 Suyak metabolizmi", "🧪 Koagulyatsiya"],
        ["🦠 Yuqumli kasalliklar", "📌 Dori nazorati"],
        ["⬅️ Orqaga", "🏠 Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_menu():
    return ReplyKeyboardMarkup([["⬅️ Orqaga", "🏠 Menu"]], resize_keyboard=True)

def get_test_buttons(info_dict):
    keys = list(info_dict.keys())
    keyboard = [keys[i:i+2] for i in range(0, len(keys), 2)]
    keyboard.append(["⬅️ Orqaga", "🏠 Menu"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
       "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n"
       "🔬 IXLA va zamonaviy texnologiyalar asosida:\n"
       "- Gormonlar\n"
       "- TORCH\n"
       "- Onkomarkerlar\n"
       "- Kardiomarkerlar\n"
       "- Umumiy qon va boshqa 200+ tahlil turini bajarish imkoniyati mavjud.\n\n"
       "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n"
       "📞 Telefon: +998 90 741 72 22\n"
       "📸 Instagram: @akmal.jon7222",
       reply_markup=get_main_menu()
    )

# --- Menyu tanlovlari ---
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    elif text == "🧪 Gormonlar":
        await update.message.reply_text("Quyidagi gormon testlaridan birini tanlang:", reply_markup=get_test_buttons(hormone_info))
    elif text == "🧫 TORCH":
        await update.message.reply_text("Quyidagi TORCH testlaridan birini tanlang:", reply_markup=get_test_buttons(torch_info))
    elif text in hormone_info:
        await update.message.reply_text(hormone_info[text], reply_markup=get_back_menu())
    elif text in torch_info:
        await update.message.reply_text(torch_info[text], reply_markup=get_back_menu())
    elif text == "📞 Admin bilan bog‘lanish":
        await update.message.reply_text("@akmaljon_lab orqali bog‘laning.", reply_markup=get_back_menu())
    elif text == "📚 Kitob haqida":
        await update.message.reply_text("Analizlar haqidagi PDF kitob narxi: 45 000 so‘m. Xarid uchun admin bilan bog‘laning.", reply_markup=get_back_menu())
    elif text in ["⬅️ Orqaga", "🏠 Menu"]:
        await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
    elif text == "🚀 Start":
        await start(update, context)
    else:
        await update.message.reply_text("Iltimos, menyudan kerakli tugmani tanlang.", reply_markup=get_main_menu())

# --- Main funksiyasi ---
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
