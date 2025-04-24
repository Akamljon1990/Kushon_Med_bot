from telegram import ReplyKeyboardMarkup

test_guruhlari_keyboard = [
    ["Gormonlar", "TORCH infeksiyalari"],
    ["Onkomarkerlar", "Kardiomarkerlar"],
    ["Biokimyo", "Umumiy qon"],
    ["Siydik", "Vitaminlar"],
    ["Orqaga"]
]

async def test_guruhlari_menu(update, context):
    reply_markup = ReplyKeyboardMarkup(test_guruhlari_keyboard, resize_keyboard=True)
    await update.message.reply_text("Test guruhini tanlang:", reply_markup=reply_markup)
