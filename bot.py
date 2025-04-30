from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- SPAM tekshiruvi ---
spam_keywords = [
    "@JetonVPNbot", "VPN", "бесплатно", "пробный период", "открыть VPN",
    "start ->", "YouTube 🚀", "Instagram ⚡", "t.me/JetonVPNbot"
]

def is_spam(text: str) -> bool:
    return any(keyword.lower() in text.lower() for keyword in spam_keywords)

# --- Tahlil ma’lumotlari (17 guruh) ---
test_info = {
    "Gormonlar": {
        "TSH": "📊 Norma: 0.27–4.2 mIU/L\n🔻 Kamaysa: gipertiroidizm\n🔺 Oshganda: gipotiroidizm"
    },
    "TORCH Paneli": {
        "Toxoplasma IgM": "📊 Norma: <0.9 IU/mL\n🔺 Yangi infeksiya belgisi"
    },
    "Onkomarkerlar": {
        "CEA": "📊 Yo‘g‘on ichak, o‘pka, ko‘krak o‘smasi aniqlashda ishlatiladi"
    },
    "Kardiomarkerlar": {
        "Troponin I": "📊 Yurak infarktini aniqlash uchun asosiy marker"
    },
    "Umumiy qon tahlili": {
        "Hb (Gemoglobin)": "📊 Erkaklar: 130–160 g/L, Ayollar: 120–140 g/L"
    },
    "Siydik tahlili": {
        "Proteinuriya": "📊 Siydikda oqsil ko‘rsatkichi buyrak kasalligidan darak"
    },
    "Biokimyo": {
        "ALT": "📊 Jigar hujayra shikastlanishini ko‘rsatadi"
    },
    "Vitaminlar": {
        "Vitamin D": "📊 30–100 ng/mL – yetarli daraja"
    },
    "Autoimmun panel": {
        "ANA": "📊 Sistematik qizil volchanka va boshqa autoimmun kasalliklarda"
    },
    "Immunoglobulinlar": {
        "IgG": "📊 Surunkali infeksiya yoki immunitet holatini ko‘rsatadi"
    },
    "Koagulyatsiya markerlari": {
        "PT (Prothrombin Time)": "📊 Qon ivish vaqtini baholaydi"
    },
    "Yuqumli kasalliklar": {
        "HBsAg": "📊 Gepatit B virusining mavjudligini bildiradi"
    },
    "Allergenlar": {
        "Total IgE": "📊 Allergik reaksiyalarni baholashda ishlatiladi"
    },
    "Dori nazorati": {
        "Digoxin": "📊 Yurak dorisi darajasini monitoring qilish"
    },
    "Suyak metabolizmi": {
        "Osteokalsin": "📊 Suyak shakllanishi markeri"
    },
    "Jigar fibrozi": {
        "FibroTest": "📊 Jigar shikastlanishi darajasini baholaydi"
    },
    "Buyrak funksiyasi": {
        "Kreatinin": "📊 Buyrak faoliyatini baholovchi asosiy marker"
    }
}

# --- Klaviatura ---
def get_main_menu():
    return ReplyKeyboardMarkup([
        ["📋 Tahlillar haqida", "📊 Tahlil natijalari"],
        ["ℹ️ Biz haqimizda", "❓ Nima bezovta qilmoqda?"],
        ["📚 Tahlillar kitobi", "🚀 Botni ulashing"],
        ["⬅️ Orqaga", "🏠 Bosh menyu"]
    ], resize_keyboard=True)

def get_analysis_menu():
    keyboard = [[guruh] for guruh in test_info.keys()]
    keyboard.append(["⬅️ Orqaga", "🏠 Bosh menyu"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_test_buttons(guruh_nomi):
    keys = list(test_info[guruh_nomi].keys())
    keyboard = [keys[i:i+2] for i in range(0, len(keys), 2)]
    keyboard.append(["⬅️ Orqaga", "🏠 Bosh menyu"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- /start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Assalomu alaykum!\n"
        "Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n\n"
        "🔬 IXLA texnologiyasi asosida 200+ testlar\n"
        "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida\n"
        "📞 +998 90 741 72 22\n"
        "📸 Instagram: @akmal.jon7222",
        reply_markup=get_main_menu()
    )

# --- Menyu tanlovlari ---
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Spam filtr
    if is_spam(text):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"Spam o‘chirishda xato: {e}")
        return

    # Menyular
    if text == "📋 Tahlillar haqida":
        await update.message.reply_text("Quyidagi tahlil guruhlaridan birini tanlang:", reply_markup=get_analysis_menu())
    elif text in test_info:
        await update.message.reply_text(f"{text} testlari:", reply_markup=get_test_buttons(text))
    elif any(text in guruh for guruh in test_info.values()):
        for guruh in test_info.values():
            if text in guruh:
                await update.message.reply_text(guruh[text], reply_markup=get_back_menu())
                break
    elif text == "📊 Tahlil natijalari":
        await update.message.reply_text("Tahlil natijalarini olish uchun ID raqamingizni kiriting.", reply_markup=get_back_menu())
    elif text == "ℹ️ Biz haqimizda":
        await update.message.reply_text("Kushon Medical Servis – 15 yillik tajriba, zamonaviy analizatorlar.", reply_markup=get_back_menu())
    elif text == "❓ Nima bezovta qilmoqda?":
        await update.message.reply_text("Bezovta qilayotgan alomatlaringizni yozing. Maslahat beramiz.", reply_markup=get_back_menu())
    elif text == "📚 Tahlillar kitobi":
        await update.message.reply_text("Tahlillar haqida to‘liq kitob (PDF): 45 000 so‘m. Admin bilan bog‘laning.", reply_markup=get_back_menu())
    elif text == "🚀 Botni ulashing":
        await update.message.reply_text("Do‘stlaringizga ham ushbu botni tavsiya qiling!", reply_markup=get_back_menu())
    elif text in ["⬅️ Orqaga", "🏠 Bosh menyu"]:
        await update.message.reply_text("Bosh menyuga qaytdingiz.", reply_markup=get_main_menu())
    else:
        await update.message.reply_text("Iltimos, menyudan biror tugmani tanlang.", reply_markup=get_main_menu())

def get_back_menu():
    return ReplyKeyboardMarkup([["⬅️ Orqaga", "🏠 Bosh menyu"]], resize_keyboard=True)

# --- Main ---
def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Bot token topilmadi. Iltimos .env faylga TOKEN yozing.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.run_polling()

if __name__ == "__main__":
    main()
