from telegram import Bot

from dtb.settings import TELEGRAM_TOKEN


def send_message(chat_id, message):
    bot = Bot(TELEGRAM_TOKEN)
    bot.send_message(chat_id, message)