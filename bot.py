from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if is_spam(text):
        try:
            await update.message.delete()
        except:
            pass
        return

    # --- Tahlillar bo‘limlari (ilgari yozilgan kod) ---
    if text == "📋 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    # … boshqa test guruhlari va test nomlari uchun kodlar …

   
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.", reply_markup=get_main_menu())
# --- Spamga qarshi sozlamalar ---
spam_keywords = [
    "@JetonVPNbot", "VPN", "бесплатно", "пробный период", "открыть VPN",
    "start ->", "YouTube 🚀", "Instagram ⚡", "t.me/JetonVPNbot"
]

def is_spam(text: str) -> bool:
    return any(keyword.lower() in text.lower() for keyword in spam_keywords)

# --- Testlar haqida qisqacha ma'lumotlar ---
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
    keyboard = [["📋 Tahlillar"]]
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

# --- Start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!",
        reply_markup=get_main_menu()
    )

# --- Menyu tanlovlari ---
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if is_spam(text):
        try:
            await update.message.delete()
        except:
            pass
        return

    if text == "📋 Tahlillar":
        await update.message.reply_text("Tahlillar guruhini tanlang:", reply_markup=get_analysis_menu())
    elif text == "🧪 Gormonlar":
        await update.message.reply_text("Gormon testini tanlang:", reply_markup=get_test_buttons(hormone_info))
    elif text == "🧫 TORCH":
        await update.message.reply_text("TORCH testini tanlang:", reply_markup=get_test_buttons(torch_info))
    elif text == "🧬 Onkomarkerlar":
        await update.message.reply_text("Onkomarker testini tanlang:", reply_markup=get_test_buttons(oncomarker_info))
    elif text == "❤️ Kardiomarkerlar":
        await update.message.reply_text("Kardiomarker testini tanlang:", reply_markup=get_test_buttons(cardiomarker_info))
    elif text == "🧪 Biokimyo":
        await update.message.reply_text("Biokimyoviy testni tanlang:", reply_markup=get_test_buttons(biochemistry_info))
    elif text == "🩸 Umumiy qon":
        await update.message.reply_text("Umumiy qon testini tanlang:", reply_markup=get_test_buttons(hematology_info))
    elif text == "🚽 Siydik tahlili":
        await update.message.reply_text("Siydik testini tanlang:", reply_markup=get_test_buttons(urine_info))
    elif text == "💊 Vitaminlar":
        await update.message.reply_text("Vitamin testini tanlang:", reply_markup=get_test_buttons(vitamin_info))
    elif text == "🧫 Autoimmun markerlar":
        await update.message.reply_text("Autoimmun testni tanlang:", reply_markup=get_test_buttons(autoimmune_info))
    elif text == "🧷 Immunoglobulinlar":
        await update.message.reply_text("Immunoglobulin testini tanlang:", reply_markup=get_test_buttons(immunoglobulin_info))
    elif text == "🦴 Suyak metabolizmi":
        await update.message.reply_text("Suyak testini tanlang:", reply_markup=get_test_buttons(bone_info))
    elif text == "🧪 Koagulyatsiya":
        await update.message.reply_text("Koagulyatsiya testini tanlang:", reply_markup=get_test_buttons(coagulation_info))
    elif text == "🦠 Yuqumli kasalliklar":
        await update.message.reply_text("Yuqumli testni tanlang:", reply_markup=get_test_buttons(infection_info))
    elif text == "📌 Dori nazorati":
        await update.message.reply_text("Dori monitoring testini tanlang:", reply_markup=get_test_buttons(drug_info))
    elif text == "🦠 Revmatologik markerlar":
        await update.message.reply_text("Revmatologik testni tanlang:", reply_markup=get_test_buttons(rheumatology_info))
    elif text == "🧬 Genetik testlar":
        await update.message.reply_text("Genetik testni tanlang:", reply_markup=get_test_buttons(genetic_info))
    elif text == "🌿 Allergik testlar":
        await update.message.reply_text("Allergik testni tanlang:", reply_markup=get_test_buttons(allergy_info))
    elif text in hormone_info:
        await update.message.reply_text(hormone_info[text])
    elif text in torch_info:
        await update.message.reply_text(torch_info[text])
    elif text in oncomarker_info:
        await update.message.reply_text(oncomarker_info[text])
    elif text in cardiomarker_info:
        await update.message.reply_text(cardiomarker_info[text])
    elif text in biochemistry_info:
        await update.message.reply_text(biochemistry_info[text])
    elif text in hematology_info:
        await update.message.reply_text(hematology_info[text])
    elif text in urine_info:
        await update.message.reply_text(urine_info[text])
    elif text in vitamin_info:
        await update.message.reply_text(vitamin_info[text])
    elif text in autoimmune_info:
        await update.message.reply_text(autoimmune_info[text])
    elif text in immunoglobulin_info:
        await update.message.reply_text(immunoglobulin_info[text])
    elif text in bone_info:
        await update.message.reply_text(bone_info[text])
    elif text in coagulation_info:
        await update.message.reply_text(coagulation_info[text])
    elif text in infection_info:
        await update.message.reply_text(infection_info[text])
    elif text in drug_info:
        await update.message.reply_text(drug_info[text])
    elif text in rheumatology_info:
        await update.message.reply_text(rheumatology_info[text])
    elif text in genetic_info:
        await update.message.reply_text(genetic_info[text])
    elif text in allergy_info:
        await update.message.reply_text(allergy_info[text])
    elif text == "⬅️ Orqaga":
        await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
   elif text == "Biz bilan bog‘lanish":
    await update.message.reply_text(
        "📞 Telefon: +998 90 741 72 22\n"
        "📍 Manzil: Kosonsoy tumani, Kattalar poliklinikasi yonida",
        reply_markup=get_main_menu()
    )
elif text == "Instagram":
    await update.message.reply_text(
        "📸 Instagram: https://instagram.com/akmal.jon7222",
        reply_markup=get_main_menu()
    )
elif text == "Admin bilan bog‘lanish":
    await update.message.reply_text(
        "🔧 Admin: @YourAdminUsername",
        reply_markup=get_main_menu()
    )
elif text == "Tahlil natijalari":
    await update.message.reply_text(
        "📝 Tahlil raqamingizni yoki PDF faylini yuboring.",
        reply_markup=get_main_menu()
    )
elif text == "Taklif va shikoyat":
    await update.message.reply_text(
        "✉️ Taklif va shikoyatingizni yozib yuboring.",
        reply_markup=get_main_menu()
    )
elif text == "Qon topshirishga tayyorgarlik":
    await update.message.reply_text(
        "💉 Qon topshirishdan 8–12 soat oldin och qoling va suyuqlik ko‘p iching.",
        reply_markup=get_main_menu()
    )
elif text == "IXLA va IFA farqi":
    await update.message.reply_text(
        "🔬 IXLA va IFA — immunotestlar farqi:\nIXLA – rangli reaksiyalar,\nIFA – fluoresensiya asosida aniqlash.",
        reply_markup=get_main_menu()
    )

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
