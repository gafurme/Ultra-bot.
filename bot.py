import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8920659123:AAGGHY7-jOneFvjtHagz7psthRZkWdh14lw"
ADMIN_ID = 359301058  # Sizning Admin ID raqamingiz

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    
    def log_message(self, format, *args):
        pass

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def set_bot_commands(application):
    commands = [
        BotCommand("start", "Botni ishga tushirish"),
        BotCommand("catalog", "📦 Ulgurji katalog"),
        BotCommand("help", "🛠 Yordam")
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n\n"
        "**ULTRA MOBILE ACCESSORIES** B2B ulgurji buyurtmalar botining beta versiyasiga xush kelibsiz.\n\n"
        "Iltimos, avvalo do'koningiz (yoki savdo nuqtangiz) nomini yuboring, shundan so'ng katalogdan foydalanishingiz mumkin:"
    )

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    catalog_text = (
        "📦 **ULTRA MOBILE ACCESSORIES — Ulgurji Katalog (Beta)**\n\n"
        "1. 🎧 **Bluetooth Naushniklar (Pro seriya)**\n"
        "   • Qoldiq: 59 dona\n"
        "   • Narxi: 59,000 so'm\n\n"
        "2. 🔌 **Type-C Fast Charge Kabel (1m)**\n"
        "   • Qoldiq: 120 dona\n"
        "   • Narxi: 12,000 so'm\n\n"
        "3. 🔋 **Adapter 20W (USB-C block)**\n"
        "   • Qoldiq: 45 dona\n"
        "   • Narxi: 35,000 so'm\n\n"
        "4. 📱 **Himoya oynasi (Glass Hydrogel)**\n"
        "   • Qoldiq: 200 dona\n"
        "   • Narxi: 8,000 so'm\n\n"
        "💡 *Buyurtma berish yoki narxlarni tasdiqlash uchun admin bilan bog'laning.*"
    )
    await update.message.reply_text(catalog_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 **Yordam bo'limi**\n\n"
        "• Do'koningiz nomini yuborib ro'yxatdan o'ting.\n"
        "• `/catalog` buyrug'i orqali joriy mahsulotlar va ulgurji narxlarni ko'ring.\n"
        "• Savollar bo'yicha adminga murojaat qiling."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await update.message.reply_text(
        f"Do'kon nomi qabul qilindi: **{text}**\n\n"
        "Endi `/catalog` buyrug'i orqali mahsulotlar narxlari bilan tanishishingiz mumkin. Tez orada adminlarimiz siz bilan bog'lanishadi."
    )

    admin_message = (
        f"🚨 **Yangi mijoz murojaati (Beta)!**\n\n"
        f"👤 Ismi: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Yo‘q'}\n"
        f"🆔 ID: `{user.id}`\n"
        f"🏢 Do'kon nomi: {text}"
    )
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Adminga xabar yuborishda xatolik: {e}")

async def main():
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    await set_bot_commands(app)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot va HTTP server muvaffaqiyatli ishga tushdi...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    asyncio.run(main())
