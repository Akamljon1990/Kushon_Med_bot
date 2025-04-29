
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- Spam aniqlash sozlamalari ---
spam_keywords = [
    "@JetonVPNbot", "VPN", "бесплатно", "пробный период", "открыть VPN",
    "start ->", "YouTube 🚀", "Instagram ⚡", "t.me/JetonVPNbot"
]

def is_spam(text: str) -> bool:
    return any(keyword.lower() in text.lower() for keyword in spam_keywords)

# --- TORCH test ma'lumotlari ---
torch_info = {
    "Toxoplasma IgM": (
        "📊 Norma: Manfiy (<0.9 IU/mL)\n"
        "🔻 Kam: Yangi infeksiya aniqlanmagan\n"
        "🔺 Ijobiy: Yaqinda Toxoplasma infeksiya\n"
        "⚡ Belgilar: Odatda simptomsiz, ba'zida limfadenopatiya\n"
        "🧪 Qachon tekshiriladi: Homiladorlikda yoki immuniteti pasayganlarda\n"
        "📈 Ijobiy: Homila uchun xavf\n"
        "📉 Manfiy: Faol infeksiya yo‘q\n"
        "🩼 Qo‘shimcha: IgG va avidity testi bilan tasdiqlash"
    ),
    "Toxoplasma IgG": (
        "📊 Norma: Manfiy (<0.9 IU/mL)\n"
        "🔻 Kamaysa: Immunitet shakllanmagan\n"
        "🔺 Ijobiy: O‘tkazilgan Toxoplasma infeksiyasi\n"
        "⚡ Belgilar: Ko‘pincha simptomsiz\n"
        "🧪 Qachon tekshiriladi: Homiladorlik va immunosupressiya holatida\n"
        "📈 Ijobiy: Immunitet bor\n"
        "📉 Manfiy: Infeksiya xavfi mavjud\n"
        "🩼 Qo‘shimcha: IgM bilan birga baholash zarur"
    )
}

# --- Klaviatura funksiyalari ---
def get_main_menu():
    keyboard = [
        ["🏠 Menu", "⬅️ Orqaga"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Xush kelibsiz!",
        reply_markup=get_main_menu()
    )

# --- Xabarlar bilan ishlovchi funksiya ---
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # SPAM aniqlash va o'chirish
    if is_spam(text):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"Spam o'chirishda xatolik: {e}")
        return

    if text == "🏠 Menu":
        await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
    elif text == "⬅️ Orqaga":
        await update.message.reply_text("Oldingi menyuga qaytdingiz.", reply_markup=get_main_menu())
    elif text in torch_info:
        await update.message.reply_text(torch_info[text], reply_markup=get_main_menu())
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.", reply_markup=get_main_menu())

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
