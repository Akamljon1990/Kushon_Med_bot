import logging
from aiogram import Bot, Dispatcher, types, executor

# Token va admin
TOKEN = "7810717425:AAGstFnjB53rmO0vfQoIPW5AhnEtOr9Vao4"
ADMIN = '@Akmaljon_lab'

# Bot va dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Loglar uchun
logging.basicConfig(level=logging.INFO)

# Start komandasi
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer_photo(
        photo=open,
        caption="👋 Assalomu alaykum!\n\n"
                "Kushon Medical Servis laboratoriyasiga xush kelibsiz!\n"
                "Eng aniq va zamonaviy diagnostika siz uchun! 🧬🔬\n\n"
                "⬇️ Quyidagi menyudan kerakli bo'limni tanlang.",
        reply_markup=start_buttons()
    )

# Asosiy menyu tugmalari
def start_buttons():
    buttons = [
        [types.KeyboardButton("🧪 Gormonlar"), types.KeyboardButton("👶 TORCH infektsiyalar")],
        [types.KeyboardButton("🔬 Onkomarkerlar"), types.KeyboardButton("❤️ Kardiomarkerlar")],
        [types.KeyboardButton("🧬 Umumiy qon tahlili"), types.KeyboardButton("💊 Biokimyo")],
        [types.KeyboardButton("🦴 Vitamin va anemiya"), types.KeyboardButton("🦠 Infeksiya tahlillari")],
        [types.KeyboardButton("ℹ️ Biz haqimizda"), types.KeyboardButton("👨‍⚕️ Admin bilan bog‘lanish")]
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in buttons:
        keyboard.add(*row)
    return keyboard

# Admin bilan bog‘lanish
@dp.message_handler(lambda message: message.text == "👨‍⚕️ Admin bilan bog‘lanish")
async def admin_contact(message: types.Message):
    await message.answer(f"Admin bilan bog‘lanish uchun: {ADMIN}")

# Biz haqimizda
@dp.message_handler(lambda message: message.text == "ℹ️ Biz haqimizda")
async def about_us(message: types.Message):
    await message.answer(
        "📍 Kushon Medical Servis - zamonaviy laboratoriya.\n\n"
        "Bizda gormonlar, TORCH infektsiyalar, onkomarkerlar, umumiy qon tahlili va ko'plab boshqa tahlillar amalga oshiriladi.\n"
        "Sifat va aniqlik kafolatlangan! 🔬🧪"
    )

# Tugmalar uchun handlerlar (gormonlar, torch va hokazo)
@dp.message_handler(lambda message: message.text in ["🧪 Gormonlar", "👶 TORCH infektsiyalar", "🔬 Onkomarkerlar", "❤️ Kardiomarkerlar", "🧬 Umumiy qon tahlili", "💊 Biokimyo", "🦴 Vitamin va anemiya", "🦠 Infeksiya tahlillari"])
async def group_selected(message: types.Message):
    await message.answer(f"Tanlangan bo‘lim: {message.text}\n\nIltimos, kerakli testni tanlang... (Yaqinda testlar ro'yxati chiqadi!)")

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
