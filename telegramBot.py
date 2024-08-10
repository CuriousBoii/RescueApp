from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your rescue bot.")

def main() -> None:
    builder = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN")
    builder.add_handler(CommandHandler("start", start))

    application = builder.build()
    application.run_polling()

if __name__ == '__main__':
    main()