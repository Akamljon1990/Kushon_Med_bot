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
