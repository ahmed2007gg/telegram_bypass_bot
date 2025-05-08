
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram.ext import ContextTypes

# اختصار الرابط باستخدام خدمة TinyURL
def shorten_url(url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        return response.text  # رابط مختصر جديد
    except requests.exceptions.RequestException as e:
        return "حدث خطأ أثناء محاولة اختصار الرابط."

# وظيفة للتعامل مع الرسائل التي تحتوي على روابط
async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "http://" in text or "https://" in text:  # التأكد من وجود رابط
        if 'bit.ly' in text or 'tinyurl' in text:  # إذا كان الرابط مختصرًا
            response = requests.get(text, allow_redirects=True)
            final_url = response.url  # الرابط النهائي بعد التوجيه
            await update.message.reply_text(f"تم تخطي الرابط! الرابط النهائي هو: {final_url}")
        else:
            shortened_url = shorten_url(text)  # اختصار الرابط
            await update.message.reply_text(f"تم اختصار الرابط إلى: {shortened_url}")
    else:
        await update.message.reply_text("لم يتم العثور على رابط صالح في رسالتك.")

# دالة لعرض الخيارات عبر الأزرار
async def show_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("اختصار الرابط", callback_data='shorten')],
        [InlineKeyboardButton("تخطي الرابط", callback_data='skip')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('اختر الخيار:', reply_markup=reply_markup)

# التعامل مع الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # الرد على الضغط على الزر
    
    if query.data == 'shorten':
        await query.edit_message_text("سيتم اختصار الرابط.")
    elif query.data == 'skip':
        await query.edit_message_text("سيتم تخطي الرابط.")

# الإعدادات للبوت
def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # إضافة مستمعين للأوامر
    application.add_handler(CommandHandler("start", show_options))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links))
    application.add_handler(CallbackQueryHandler(button_handler))

    # بدء تشغيل البوت
    application.run_polling()

if __name__ == '__main__':
    main()
