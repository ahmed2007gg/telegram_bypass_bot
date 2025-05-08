import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 تخطي رابط", callback_data='skip')],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data='settings')],
        [InlineKeyboardButton("ℹ️ حول البوت", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك! اختر أحد الخيارات:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'skip':
        await query.edit_message_text("أرسل الرابط المختصر الآن وسأتولى تخطيه.")
    elif query.data == 'settings':
        await query.edit_message_text("🚧 إعدادات البوت قيد التطوير.")
    elif query.data == 'about':
        await query.edit_message_text("🤖 هذا البوت يساعدك على تخطي الروابط المختصرة بسرعة.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ البوت يعمل الآن.")
    app.run_polling()

if __name__ == '__main__':
    main()
