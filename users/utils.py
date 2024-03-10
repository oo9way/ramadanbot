from telegram import Bot

from dtb.settings import TELEGRAM_TOKEN

TELEGRAM_TOKEN = "6432845948:AAHqwCgoO-J7fWkOO3E7fDHoqCdeE5I6wXI"
def send_message(chat_id, message):
    bot = Bot(TELEGRAM_TOKEN)
    bot.send_message(chat_id, message)