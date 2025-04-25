import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from Menu import main_menu

# /start buyruği bosilganda ishlovchi funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Salmomalaykum xabari va menyuni yuboradi."""
    welcome_text = (
        "Assalomu alaykum! Kushon Medical Servis botiga xush kelibsiz! "
        "Zamonaviy laboratoriya tahlillari va ishonchli natijalar. "
        "Quyidagi bo‘limlardan keraklisini tanlang."
    )
    # Yuqoridagi matnni foydalanuvchiga yuborish (asosiy menyu bilan birga)
    await update.message.reply_text(welcome_text, reply_markup=main_menu)

# Foydalanuvchi menyudan tanlov qilganda ishlovchi funksiya
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menyudan tanlangan bo'limlarga javob beradi."""
    user_choice = update.message.text
    response_text = ""
    # Foydalanuvchi tanloviga qarab javob tayyorlash
    if user_choice == "Tahlillar":
        response_text = "Siz 'Tahlillar' bo‘limini tanladingiz."
        # (Bu yerda mavjud tahlillar ro‘yxatini chiqarish mumkin)
    elif user_choice == "Biz bilan bog‘lanish":
        response_text = ("Biz bilan bog‘lanish: +998 (XX) XXX-XX-XX.\n"
                         "Manzil: Toshkent sh., [Manzilni kiriting].")
    elif user_choice == "Instagram manzil":
        response_text = "Instagram sahifamiz: instagram.com/kushonmedicalservis"
    elif user_choice == "Admin bilan bog‘lanish":
        response_text = "Admin bilan bog‘lanish: @YourAdminUsername"
    elif user_choice == "Tahlil natijalari":
        response_text = ("Laboratoriya natijalari bo'limi. "
                         "Natijalaringizni ko'rish uchun ID raqamingizni kiriting.")
    elif user_choice == "Taklif va shikoyat":
        response_text = "Taklif va shikoyatlaringizni shu yerga yozib yuboring."
    elif user_choice == "Qon topshirishga tayyorgarlik":
        response_text = ("Qon topshirishga tayyorgarlik bo'yicha yo'riqnoma:\n"
                         "- Tahlilga kelishdan oldin 8-12 soat ovqat yemang (och qoringa keling).\n"
                         "- Laboratoriya oldidan choy yoki qahva ichmang, faqat suv ichish mumkin.")
    elif user_choice == "IXLA va IFA tekshiruv farqi":
        response_text = ("IXLA (Immunoxemiluminessensiya) va IFA (Immunoferment analiz) farqi:\n"
                         "- IXLA zamonaviy usul bo'lib, luminessensiya orqali antitana va antigenlarni aniqlaydi.\n"
                         "- IFA esa ferment reaksiyasi yordamida antitana va antigenlarni aniqlaydi.")
    else:
        # Noma’lum matn kiritilsa, foydalanuvchini menyudan tanlashga undash
        response_text = "Iltimos, menyudan bo‘lim tanlang."
    # Javob matnini foydalanuvchiga yuborish
    await update.message.reply_text(response_text)

if __name__ == "__main__":
    # .env faylidan TOKEN o'zgaruvchisini o'qish
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Bot token not found. Please set the TOKEN in the environment.")
    # Bot ilovasini yaratish
    app = ApplicationBuilder().token(token).build()
    # Handler (ishlovchi) larni ro‘yxatdan o‘tkazish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    # Botni ishga tushirish (Ctrl+C bosilgunga qadar ishlaydi)
    app.run_polling()
