from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- Spamga qarshi sozlamalar ---
spam_keywords = [
    "@JetonVPNbot", "@JetonVPNNbot", "VPN", "vpn.arturshi.ru",
    "бесплатно", "пробный период", "открыть VPN", "YouTube",
    "Instagram", "7 дней", "SmartTV", "Подключайся", "стабильный интернет"
]

def is_spam(text: str) -> bool:
    return any(keyword.lower() in text.lower() for keyword in spam_keywords)

# --- Testlar uchun ma'lumotlar ---
hormone_info = {"TSH": "📈 Norma: 0.27–4.2 mIU/L\n🔻 Kamaysa: gipertiroidizm\n🔺 Oshganda: gipotiroidizm"}
torch_info = {"Toxoplasma IgM": "📈 Norma: <0.9 IU/mL\n🔻 Kam: infeksiya yo‘q\n🔺 Ijobiy: yaqinda yuqqan"}
oncomarker_info = {"AFP": "📈 Norma: <10 ng/mL\n🔺 Oshganda: jigar o‘smalari"}

# --- Klaviatura funksiyalari ---
def get_main_menu():
    keyboard = [
        ["📄 Tahlillar", "📱 Natijani olish"],
        ["🤔 Nima bezovta qilyapti", "📄 IXLA va IFA farqi"],
        ["📖 Tahlillar kitobi (pullik)", "🔗 Ulashing"],
        ["🏠 Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_analysis_menu():
    keyboard = [
        ["🌿 Gormonlar", "🦥 TORCH"],
        ["💉 Onkomarkerlar", "❤️ Kardiomarkerlar"],
        ["📊 Umumiy qon", "🚽 Siydik tahlili"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_test_buttons(info_dict):
    keys = list(info_dict.keys())
    keyboard = [keys[i:i+2] for i in range(0, len(keys), 2)]
    keyboard.append(["⬅️ Orqaga", "🏠 Menu"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎒 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n"
        "🧬 IXLA va zamonaviy texnologiyalar asosida 200+ test mavjud.\n"
        "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n"
        "📞 Tel: +998 90 741 72 22\n"
        "📷 Instagram: @akmal.jon7222",
        reply_markup=get_main_menu()
    )

# --- Xabarlar bilan ishlash ---
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if is_spam(text):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"Spamni o'chirishda xatolik: {e}")
        return

    if text == "📄 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    elif text == "🌿 Gormonlar":
        await update.message.reply_text("Gormon testini tanlang:", reply_markup=get_test_buttons(hormone_info))
    elif text == "🦥 TORCH":
        await update.message.reply_text("TORCH testini tanlang:", reply_markup=get_test_buttons(torch_info))
    elif text == "💉 Onkomarkerlar":
        await update.message.reply_text("Onkomarker testini tanlang:", reply_markup=get_test_buttons(oncomarker_info))
    elif text in hormone_info:
        await update.message.reply_text(hormone_info[text])
    elif text in torch_info:
        await update.message.reply_text(torch_info[text])
    elif text in oncomarker_info:
        await update.message.reply_text(oncomarker_info[text])
    elif text in ["⬅️ Orqaga", "🏠 Menu"]:
        await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.", reply_markup=get_main_menu())

# --- Main ---
def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError(".env faylda TOKEN yo‘q!")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    app.run_polling()

if __name__ == "__main__":
    main()
