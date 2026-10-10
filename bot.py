import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8920659123:AAGGHY7-jOneFvjtHagz7psthRZkWdh14lw"
ADMIN_ID = 359301058

# Render port talabini qondirish uchun oddiy HTTP server (qo'shimcha kutubxona shart emas)
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

async def main():
    # HTTP serverni alohida oqimda ishga tushiramiz (Render port talabi uchun)
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    # Telegram botni ishga tushiramiz
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot va HTTP server muvaffaqiyatli ishga tushdi...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Dastur to'xtab qolmasligi uchun
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    asyncio.run(main())
