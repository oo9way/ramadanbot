from telegram import  Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from users.models import User
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

RAMADANDAYS, PAYMENT, LOCATION, ACCEPT_CHECK, CHOOSE_PAYMENT, CASH, CARD = range(7)


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(
        text +
        f"\nKontaktni yuboring.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Telefon raqamni yuborish", request_contact=True)]]
        ))

    return RAMADANDAYS


def ramadan_days(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Ramadan days %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ramazonning qaysi kunlarida qatnashmoqchisiz ?, '
        'Ushbu formatda yuboring, 10-20 yoki 1-15, yoki 1-30 (Boshlash kuni-Tugash kuni)',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PAYMENT


def payment(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    text = update.message.text.split("-")
    days = (int(text[1]) - int(text[0]) + 1)
    summa = days * 7000
    keyboard = [['Naqd', 'Card']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        f'{days} kun! Jami to`lov {summa} so`m.',
        reply_markup=reply_markup
    )

    return CHOOSE_PAYMENT


def choose_payment(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    text = update.message.text
    if text == "Naqd":
        update.message.reply_text(
            f'Naqd to`lash so`rovingiz qabul qilindi. Tashakkur ).',
        )
    elif text == "Card":
        update.message.reply_text(
            'Iltimos to`lov chekini rasm ko`rinishida yuboring.'
        )

        return ACCEPT_CHECK

    return ConversationHandler.END


def accept_check(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    update.message.reply_text(
        'Qabul uchun so`rov yuborildi, tashakkur.'
    )

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
