from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import re

# --- Environment variables ---
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Bot token topilmadi. .env faylga TOKEN kiriting.")
# Render specific: external URL and port
PORT = int(os.getenv("PORT", "8443"))
BASE_URL = os.getenv("RENDER_EXTERNAL_URL")  # e.g., https://your-app.onrender.com
if not BASE_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL environment variable not set.")
WEBHOOK_URL = f"{BASE_URL}/{TOKEN}"

# --- Spam sozlamalari ---
spam_keywords = [
    "@JetonVPNbot", "VPN", "бесплатно", "пробный период", "открыть VPN",
    "start ->", "YouTube 🚀", "Instagram ⚡", "t.me/JetonVPNbot"
]
url_pattern = re.compile(r"https?://\S+")
bot_link_pattern = re.compile(r"@[A-Za-z0-9_]+bot")

def is_spam(text: str) -> bool:
    txt = text.lower()
    if any(keyword.lower() in txt for keyword in spam_keywords):
        return True
    if url_pattern.search(text):
        return True
    if bot_link_pattern.search(text):
        return True
    return False

# --- Testlar ma'lumotlari ---
# ... lug'atlar bir xil ... (hormone_info, torch_info, ... allergy_info) ...
# klaviatura funksiyalari: get_main_menu(), get_analysis_menu(), get_test_buttons()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Assalomu alaykum! Kushon Medical Servis laboratoriyasiga xush kelibsiz!",
        reply_markup=get_main_menu()
    )

async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if is_spam(text):
        try:
            await update.message.delete()
        except:
            pass
        return
    # menyu logikasi ...

# --- Application setup ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))

# --- Webhook start ---
async def on_startup(app):
    await app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    # Set webhook and start
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_init=on_startup
    )
