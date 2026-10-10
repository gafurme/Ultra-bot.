import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sizning tokeningiz
TOKEN = "8920659123:AAE9S1djLfoh7Hj-3zDgDLBVMGKqBLFsuxa"

# Sizning Telegram ID raqamingiz (Admin)
ADMIN_ID = 359301058  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n\n"
        "**ULTRA MOBILE ACCESSORIES** ulgurji buyurtma botiga xush kelibsiz. 🔌📱\n\n"
        "Iltimos, hamkorlikni boshlash uchun **Do'koningiz nomi**, **Manzilingiz** va **Telefon raqamingizni** yuboring:\n"
        "*(Masalan: 'Nur do'koni, Samarqand sh., +998901234567)*"
    )
    context.user_data['waiting_for_info'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_info'):
        store_info = update.message.text
        user = update.effective_user
        
        admin_text = (
            f"📥 **Yangi do'kon ro'yxatdan o'tishni so'raydi!**\n\n"
            f"👤 Foydalanuvchi: {user.full_name} (@{user.username if user.username else 'yoq'})\n"
            f"🆔 ID: `{user.id}`\n"
            f"📋 Ma'lumot: {store_info}"
        )
        
        keyboard = [
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user.id}")],
            [InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID, 
                text=admin_text, 
                reply_markup=reply_markup, 
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Adminga yuborishda xatolik: {e}")

        await update.message.reply_text(
            "Rahmat! Ma'lumotlaringiz qabul qilindi. Menejerimiz tez orada profilingizni tekshirib tasdiqlaydi."
        )
        context.user_data['waiting_for_info'] = False

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data.startswith("approve_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="🎉 Tabriklaymiz! Sizning do'koningiz tasdiqlandi. Endi kanaldagi mahsulotlarni osongina bron qilishingiz mumkin."
        )
        await query.edit_message_text(text="✅ Ushbu do'kon tasdiqlandi!")
        
    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="Kechirasiz, ma'lumotlaringiz tasdiqlanmadi. Iltimos, menejer bilan bog'laning."
        )
        await query.edit_message_text(text="❌ Rad etildi.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()
