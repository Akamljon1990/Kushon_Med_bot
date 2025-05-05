from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import re

# --- Spam sozlamalari ---
spam_keywords = [
    "@JetonVPNbot", "VPN", "бесплатно", "пробный период", "открыть VPN",
    "start ->", "YouTube 🚀", "Instagram ⚡", "t.me/JetonVPNbot"
]
# URL va bot havolalarini aniqlash uchun regex
url_pattern = re.compile(r"https?://\S+")
bot_link_pattern = re.compile(r"@[A-Za-z0-9_]+bot")

def is_spam(text: str) -> bool:
    txt = text.lower()
    # Kalit so'zlar bo'yicha tekshiruv
    if any(keyword.lower() in txt for keyword in spam_keywords):
        return True
    # URL mavjud bo'lsa
    if url_pattern.search(text):
        return True
    # Bot username havolasi bo'lsa
    if bot_link_pattern.search(text):
        return True
    return False

# --- Testlar haqida ma'lumot lug'atlari ---
hormone_info = {"TSH": "📊 Norma: 0.27–4.2 mIU/L\n🔻 Kamaysa: gipertiroidizm\n🔺 Oshganda: gipotiroidizm"}
torch_info = {"Toxoplasma IgM": "📊 Norma: <0.9 IU/mL\n🔺 Yaqinda infeksiya"}
oncomarker_info = {"AFP": "📊 Norma: <10 ng/mL\n🔺 Oshganda: jigar kasalliklari"}
cardiomarker_info = {"Troponin I": "📊 Norma: <0.04 ng/mL\n🔺 Oshganda: infarkt"}
biochemistry_info = {"Glucose": "📊 Norma: 3.9–5.8 mmol/L"}
hematology_info = {"Hemoglobin": "📊 Norma: erkaklar 130–160 g/L, ayollar 120–150 g/L"}
urine_info = {"Protein": "📊 Norma: Manfiy\n🔺 Oshganda: buyrak shikastlanishi"}
vitamin_info = {"Vitamin D": "📊 Norma: 30–100 ng/mL"}
autoimmune_info = {"ANA": "📊 Norma: Manfiy\n🔺 Oshganda: SLE, AR"}
immunoglobulin_info = {"IgG": "📊 Norma: 700–1600 mg/dL"}
bone_info = {"Calcium": "📊 Norma: 2.2–2.6 mmol/L"}
coagulation_info = {"INR": "📊 Norma: 0.8–1.2"}
infection_info = {"CRP": "📊 Norma: <5 mg/L\n🔺 Yallig'lanishda oshadi"}
drug_info = {"Paracetamol": "📊 Terapevtik daraja: 10–30 mg/L"}
rheumatology_info = {"RF": "📊 Norma: <14 IU/mL\n🔺 Revmatoyd artritda oshadi"}
genetic_info = {"CFTR": "📊 Sistik fibroz uchun genetik test"}
allergy_info = {"IgE": "📊 Norma: 0–100 IU/mL\n🔺 Allergiyada oshadi"}

# --- Klaviatura funksiyalari ---
def get_main_menu():
    keyboard = [
        ["📋 Tahlillar", "Biz bilan bog‘lanish"],
        ["Instagram", "Admin bilan bog‘lanish"],
        ["Tahlil natijalari", "Taklif va shikoyat"],
        ["Qon topshirishga tayyorgarlik", "IXLA va IFA farqi"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_analysis_menu():
    keyboard = [
        ["🧪 Gormonlar", "🧫 TORCH"],
        ["🧬 Onkomarkerlar", "❤️ Kardiomarkerlar"],
        ["🧪 Biokimyo", "🩸 Umumiy qon"],
        ["🚽 Siydik tahlili", "💊 Vitaminlar"],
        ["🧫 Autoimmun markerlar", "🧷 Immunoglobulinlar"],
        ["🦴 Suyak metabolizmi", "🧪 Koagulyatsiya"],
        ["🦠 Yuqumli kasalliklar", "📌 Dori nazorati"],
        ["🦠 Revmatologik markerlar", "🧬 Genetik testlar"],
        ["🌿 Allergik testlar", "⬅️ Orqaga"]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_test_buttons(info_dict):
    keys = list(info_dict.keys())
    keyboard = [keys[i:i + 2] for i in range(0, len(keys), 2)]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- /start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!",
        reply_markup=get_main_menu()
    )

# --- Xabarlarni qayta ishlash ---
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if is_spam(text):
        try:
            await update.message.delete()
        except:
            pass
        return

    # Botning odatiy menyu logikasi quyida davom etadi...
    if text == "📋 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    # ... qolgan kod o'zgarmadi...

# --- Dastur ishga tushishi ---
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
