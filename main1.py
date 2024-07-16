from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

TOKEN = '7415903848:AAEoQ5jVnhXxEQgp4RbAfBddGEM5tIA_Qpw'

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    print(f"Received /start command from chat ID: {chat_id}")
    await update.message.reply_text(f"Your chat ID is {chat_id}")

def main():
    print("Starting bot...")
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    print("Running polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
