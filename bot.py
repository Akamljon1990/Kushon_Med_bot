from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

# 1. Asosiy menyu tugmalari
main_menu_keyboard = [
    ["Tahlillar", "Biz bilan bog‘lanish"],
    ["Instagram manzil", "Admin bilan bog‘lanish"],
    ["Tahlil natijalari", "Taklif va shikoyat"],
    ["Qon topshirishga tayyorgarlik", "IXLA va IFA tekshiruv farqi"]
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# 2. Tahlillar menyusi
tahlillar_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("1. Gormonlar", callback_data='gormonlar')],
    [InlineKeyboardButton("2. TORCH paneli", callback_data='torch')],
    [InlineKeyboardButton("3. Onkomarkerlar", callback_data='onkomarker')],
    [InlineKeyboardButton("4. Vitaminlar va Anemiya", callback_data='vitamin')],
    [InlineKeyboardButton("5. Kardiomarkerlar", callback_data='kardio')],
    [InlineKeyboardButton("6. Koagulyatsiya", callback_data='koagul')],
    [InlineKeyboardButton("7. Suyak metabolizmi", callback_data='suyak')],
    [InlineKeyboardButton("8. Jigar fibrozi", callback_data='jigar')],
    [InlineKeyboardButton("9. Buyrak funksiyasi", callback_data='buyrak')],
    [InlineKeyboardButton("10. Immunoglobulinlar", callback_data='immun')],
    [InlineKeyboardButton("11. Autoimmun panel", callback_data='autoimmun')],
    [InlineKeyboardButton("12. Yuqumli kasalliklar", callback_data='infeksiya')],
    [InlineKeyboardButton("13. Allergenlar", callback_data='allergen')],
    [InlineKeyboardButton("14. Dori nazorati", callback_data='dori')]
])

# 3. start funksiyasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\nKushon Medical Servis laboratoriyasi rasmiy botiga xush kelibsiz.\nPastdagi menyudan kerakli bo‘limni tanlang 👇",
        reply_markup=main_menu
    )

# 4. Tugmalarni ishlovchi funksiya
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Tahlillar":
        await update.message.reply_text(
            "Quyidagi test guruhlaridan birini tanlang:", reply_markup=tahlillar_menu
        )
    else:
        await update.message.reply_text("Iltimos, menyudan biror bo‘limni tanlang.")

# 5. Inline tugmalarni ishlovchi funksiya (siz yuborgan qism)
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "gormonlar":
        await query.edit_message_text("🧬 Gormonlar testi qalqonsimon bez, jinsiy gormonlar, stress va boshqa organizm muvozanatini ta’minlovchi gormonlarni aniqlash uchun o‘tkaziladi.")
    elif query.data == "torch":
        await query.edit_message_text("🧫 TORCH paneli homiladorlikdagi xavfli infeksiyalarni (Toxoplasma, Rubella, CMV, Herpes) aniqlash uchun muhim testlar to‘plamidir.")
    elif query.data == "onkomarker":
        await query.edit_message_text("🎯 Onkomarkerlar orqali organizmdagi o‘sma jarayonlarini erta aniqlash va nazorat qilish imkoniyati mavjud.")
    elif query.data == "vitamin":
        await query.edit_message_text("🍀 Vitaminlar va anemiya tekshiruvi qonda vitamin yetishmovchiligi va kamqonlik belgilari haqida ma'lumot beradi.")
    elif query.data == "kardio":
        await query.edit_message_text("❤️ Kardiomarkerlar yurak mushaklari holatini baholaydi va infarkt yoki yurak xurujlarini erta aniqlashda yordam beradi.")
    elif query.data == "koagul":
        await query.edit_message_text("🩸 Koagulyatsiya testlari qoningizning ivish qobiliyatini va qon ketish xavfini aniqlashga xizmat qiladi.")
    elif query.data == "suyak":
        await query.edit_message_text("🦴 Suyak metabolizmi testlari suyak zichligi va suyak kasalliklarining erta belgilarini aniqlash uchun o‘tkaziladi.")
    elif query.data == "jigar":
        await query.edit_message_text("🫀 Jigar fibrozi tekshiruvi jigar to‘qimalaridagi shikastlanish va fibroz jarayonlarni aniqlash imkonini beradi.")
    elif query.data == "buyrak":
        await query.edit_message_text("🚰 Buyrak faoliyatini baholovchi testlar organizmdagi suyuqlik va chiqindi mahsulotlarni chiqarish salohiyatini o‘lchaydi.")
    elif query.data == "immun":
        await query.edit_message_text("🛡 Immunoglobulin testlari organizm immun javobining kuchini va infeksiyalarga qarshi kurashish imkoniyatini baholaydi.")
    elif query.data == "autoimmun":
        await query.edit_message_text("🔬 Autoimmun panel testlari tananing o‘z to‘qimalariga qarshi xato hujum qilayotgan immun kasalliklarini aniqlashda yordam beradi.")
    elif query.data == "infeksiya":
        await query.edit_message_text("🦠 Yuqumli kasalliklar testi COVID-19, VICH va boshqa virusli infeksiyalarni aniqlash uchun o‘tkaziladi.")
    elif query.data == "allergen":
        await query.edit_message_text("🌸 Allergen testlari sizda allergik reaksiyaga sabab bo‘ladigan moddalarni aniqlash uchun mo‘ljallangan.")
    elif query.data == "dori":
        await query.edit_message_text("💊 Dori vositalarini nazorat qilish testi qondagi dori kontsentratsiyasini o‘lchaydi va terapiya samaradorligini baholaydi.")
    else:
        await query.edit_message_text("Tanlangan bo‘limni qayta tekshiring.")

# 6. main funksiyasi
def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
