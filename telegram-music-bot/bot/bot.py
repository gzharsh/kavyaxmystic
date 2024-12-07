import os
from telegram.ext import Updater
from dotenv import load_dotenv
from bot.handlers import setup_handlers

def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    if not TELEGRAM_TOKEN:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables.")

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    setup_handlers(dispatcher)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
