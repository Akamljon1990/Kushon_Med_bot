import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

# .env fayldan tokenni olish
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Start komandasi
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Kushon Medical Servis laboratoriya botiga xush kelibsiz!")

# Botni ishga tushurish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
