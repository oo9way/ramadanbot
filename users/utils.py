import requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from dtb.settings import TELEGRAM_TOKEN

TELEGRAM_TOKEN = "6432845948:AAHqwCgoO-J7fWkOO3E7fDHoqCdeE5I6wXI"


def send_message(chat_id, message):
    bot = Bot(TELEGRAM_TOKEN)
    bot.send_message(chat_id, message)


def send_photo(chat_id, photo, message, order_id):
    bot = Bot(TELEGRAM_TOKEN)
    photo_response = requests.get(photo)
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data=f'confirm-{order_id}')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if the request was successful
    if photo_response.status_code == 200:
        bot.send_photo(chat_id=chat_id, photo=photo_response.content, caption=message, reply_markup=reply_markup)


def send_confirm_text(chat_id, message, order_id):
    print("Text worked")
    bot = Bot(TELEGRAM_TOKEN)

    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data=f'confirm-{order_id}')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
