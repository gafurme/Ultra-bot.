import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sizning ma'lumotlaringiz
BOT_TOKEN = "8920659123:AAGGHY7-jOneFvjtHagz7psthRZkWdh14lw"
ADMIN_ID = 359301058

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n\n"
        "**ULTRA MOBILE ACCESSORIES** B2B ulgurji buyurtmalar botiga xush kelibsiz.\n"
        "Iltimos, do'koningiz (yoki savdo nuqtangiz) nomini yuboring:"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(
        f"Do'kon nomi qabul qilindi: **{text}**\n\n"
        "Tez orada adminlarimiz sizning ma'lumotlaringizni tekshirib, ulgurji narxlarni ochib berishadi."
    )

def main():
    # Event loop xatoligining oldini olish uchun
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
