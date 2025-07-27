from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7612678098:AAG8m1wxZThFox3lF7trEoZoodblI-qt1bU'

async def get_chat_id(update, context: ContextTypes.DEFAULT_TYPE):
    print(f"New message from chat ID: {update.effective_chat.id}")
    await update.message.reply_text("Thanks! You're now subscribed to alerts.")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, get_chat_id))
app.run_polling()
