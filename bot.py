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
hormone_info = {"TSH": "📊 Norma: 0.27–4.2 mIU/L\n..."}
torch_info = {"Toxoplasma IgM": "📊 Norma: <0.9 IU/mL\n..."}
oncomarker_info = {"AFP": "📊 Norma: <10 ng/mL\n..."}
cardiomarker_info = {"Troponin I": "📊 Norma: <0.04 ng/mL\n..."}
biochemistry_info = {"Glucose": "📊 Norma: 3.9–5.8 mmol/L\n..."}
hematology_info = {"Hemoglobin": "📊 Norma: erkaklar 130–170 g/L\n..."}
urine_info = {"Protein": "📊 Norma: Manfiy\n..."}
vitamin_info = {"Vitamin D": "📊 Norma: 30–100 ng/mL\n..."}
autoimmune_info = {"ANA": "📊 Norma: Manfiy\n..."}
immunoglobulin_info = {"IgG": "📊 Norma: 700–1600 mg/dL\n..."}
infectious_info = {"HCV IgG": "📊 Norma: Manfiy\n..."}
drug_info = {"Phenobarbital": "📊 Norma: 10–40 µg/mL\n..."}
allergy_info = {"Total IgE": "📊 Norma: <100 IU/mL\n..."}
coagulation_info = {"PT": "📊 Norma: 11–13.5 sek\n..."}
bone_info = {"Calcium": "📊 Norma: 2.1–2.6 mmol/L\n..."}
liver_info = {"FibroTest": "📊 Norma: <0.3\n..."}
kidney_info = {"Creatinine": "📊 Norma: erkaklar 62–106 µmol/L\n..."}

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
        ["🧪 Gormonlar", "🧫 TORCH"],
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
        "🔬 IXLA va zamonaviy texnologiyalar asosida: Gormonlar, TORCH, Onkomarkerlar, Kardiomarkerlar, va yana 200+ test\n\n"
        "📍 Manzil: Kosonsoy tumani\n📞 +998 90 741 72 22\n📸 Instagram: @akmal.jon7222",
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

    if text == "📋 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    elif text == "🧪 Gormonlar":
        await update.message.reply_text("Gormon testlarini tanlang:", reply_markup=get_test_buttons(hormone_info))
    elif text == "🧫 TORCH":
        await update.message.reply_text("TORCH testlarini tanlang:", reply_markup=get_test_buttons(torch_info))
    elif text == "💉 Onkomarkerlar":
        await update.message.reply_text("Onkomarker testlarini tanlang:", reply_markup=get_test_buttons(oncomarker_info))
    elif text == "❤️ Kardiomarkerlar":
        await update.message.reply_text("Kardiomarker testlarini tanlang:", reply_markup=get_test_buttons(cardiomarker_info))
    elif text == "🧪 Biokimyo":
        await update.message.reply_text("Biokimyoviy testlar:", reply_markup=get_test_buttons(biochemistry_info))
    elif text == "🩸 Umumiy qon":
        await update.message.reply_text("Umumiy qon testlari:", reply_markup=get_test_buttons(hematology_info))
    elif text == "🚽 Siydik tahlili":
        await update.message.reply_text("Siydik tahlili testlari:", reply_markup=get_test_buttons(urine_info))
    elif text == "💊 Vitaminlar":
        await update.message.reply_text("Vitamin testlarini tanlang:", reply_markup=get_test_buttons(vitamin_info))
    elif text == "🧬 Autoimmun":
        await update.message.reply_text("Autoimmun testlari:", reply_markup=get_test_buttons(autoimmune_info))
    elif text == "🧷 Immunoglobulinlar":
        await update.message.reply_text("Immunoglobulin testlari:", reply_markup=get_test_buttons(immunoglobulin_info))
    elif text == "🦠 Yuqumli kasalliklar":
        await update.message.reply_text("Infeksiyalarni tanlang:", reply_markup=get_test_buttons(infectious_info))
    elif text == "📌 Dori nazorati":
        await update.message.reply_text("Dori monitoringi:", reply_markup=get_test_buttons(drug_info))
    elif text == "🧪 Koagulyatsiya":
        await update.message.reply_text("Koagulyatsiya testlari:", reply_markup=get_test_buttons(coagulation_info))
    elif text == "🦴 Suyak metabolizmi":
        await update.message.reply_text("Suyak almashinuvi testlari:", reply_markup=get_test_buttons(bone_info))
    elif text == "🧪 Jigar fibrozi":
        await update.message.reply_text("Jigar testlari:", reply_markup=get_test_buttons(liver_info))
    elif text == "Buyrak funksiyasi":
        await update.message.reply_text("Buyrak testlari:", reply_markup=get_test_buttons(kidney_info))
    elif text in hormone_info:
        await update.message.reply_text(hormone_info[text], reply_markup=get_back_menu())
    elif text in torch_info:
        await update.message.reply_text(torch_info[text], reply_markup=get_back_menu())
    elif text in oncomarker_info:
        await update.message.reply_text(oncomarker_info[text], reply_markup=get_back_menu())
    elif text in cardiomarker_info:
        await update.message.reply_text(cardiomarker_info[text], reply_markup=get_back_menu())
    elif text in biochemistry_info:
        await update.message.reply_text(biochemistry_info[text], reply_markup=get_back_menu())
    elif text in hematology_info:
        await update.message.reply_text(hematology_info[text], reply_markup=get_back_menu())
    elif text in urine_info:
        await update.message.reply_text(urine_info[text], reply_markup=get_back_menu())
    elif text in vitamin_info:
        await update.message.reply_text(vitamin_info[text], reply_markup=get_back_menu())
    elif text in autoimmune_info:
        await update.message.reply_text(autoimmune_info[text], reply_markup=get_back_menu())
    elif text in immunoglobulin_info:
        await update.message.reply_text(immunoglobulin_info[text], reply_markup=get_back_menu())
    elif text in infectious_info:
        await update.message.reply_text(infectious_info[text], reply_markup=get_back_menu())
    elif text in drug_info:
        await update.message.reply_text(drug_info[text], reply_markup=get_back_menu())
    elif text in coagulation_info:
        await update.message.reply_text(coagulation_info[text], reply_markup=get_back_menu())
    elif text in bone_info:
        await update.message.reply_text(bone_info[text], reply_markup=get_back_menu())
    elif text in liver_info:
        await update.message.reply_text(liver_info[text], reply_markup=get_back_menu())
    elif text in kidney_info:
        await update.message.reply_text(kidney_info[text], reply_markup=get_back_menu())
    elif text == "📞 Admin bilan bog‘lanish":
        await update.message.reply_text("Admin: @akmaljon_lab", reply_markup=get_back_menu())
    elif text in ["⬅️ Orqaga", "🏠 Menu"]:
        await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
    elif text == "🚀 Start":
        await start(update, context)
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.", reply_markup=get_main_menu())

# --- Main ---
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
