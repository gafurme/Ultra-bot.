import logging
import asyncio
import os
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# Render port talabini qondirish uchun oddiy veb-server
async def handle_web(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app_web = web.Application()
    app_web.add_routes([web.get('/', handle_web)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Veb serverni fonda ishga tushiramiz (Render port talabi uchun)
    asyncio.create_task(web_server())

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot va veb-server muvaffaqiyatli ishga tushdi...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Dastur to'xtab qolmasligi uchun
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    asyncio.run(main())
