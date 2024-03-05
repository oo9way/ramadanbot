import os
import requests
from django.core.files import File
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from users.models import User, Application
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

RAMADANDAYS, PAYMENT, LOCATION, ACCEPT_CHECK, CHOOSE_PAYMENT, CASH, CARD = range(7)

days_keyboard = [
    [
        InlineKeyboardButton("March", callback_data="00"),
    ],
    [
        InlineKeyboardButton("10", callback_data='10'),
        InlineKeyboardButton("11", callback_data='11'),
        InlineKeyboardButton("12", callback_data='12'),
        InlineKeyboardButton("13", callback_data='13'),
        InlineKeyboardButton("14", callback_data='14'),
        InlineKeyboardButton("15", callback_data='15'),
        InlineKeyboardButton("16", callback_data='16'),
        InlineKeyboardButton("17", callback_data='17'),

    ],
    [
        InlineKeyboardButton("18", callback_data='18'),
        InlineKeyboardButton("19", callback_data='19'),
        InlineKeyboardButton("20", callback_data='20'),
        InlineKeyboardButton("21", callback_data='21'),
        InlineKeyboardButton("22", callback_data='22'),
        InlineKeyboardButton("23", callback_data='23'),
        InlineKeyboardButton("24", callback_data='24'),
        InlineKeyboardButton("25", callback_data='25'),

    ],
    [
        InlineKeyboardButton("26", callback_data='26'),
        InlineKeyboardButton("27", callback_data='27'),
        InlineKeyboardButton("28", callback_data='28'),
        InlineKeyboardButton("29", callback_data='29'),
        InlineKeyboardButton("*", callback_data='00'),
        InlineKeyboardButton("*", callback_data='00'),
        InlineKeyboardButton("*", callback_data='00'),
        InlineKeyboardButton("*", callback_data='00'),
    ],
    [
        InlineKeyboardButton("April", callback_data="00"),
    ],
    [
        InlineKeyboardButton("1", callback_data='30'),
        InlineKeyboardButton("2", callback_data='31'),
        InlineKeyboardButton("3", callback_data='32'),
        InlineKeyboardButton("4", callback_data='33'),
        InlineKeyboardButton("5", callback_data='34'),
        InlineKeyboardButton("6", callback_data='35'),
        InlineKeyboardButton("7", callback_data='36'),
        InlineKeyboardButton("8", callback_data='37'),
    ],
    [
        InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm"),
    ],
]
numbers_in_emoji = {
    "10": "1️⃣0️⃣ - mart",
    "11": "1️⃣1️⃣ - mart",
    "12": "1️⃣2️⃣ - mart",
    "13": "1️⃣3️⃣ - mart",
    "14": "1️⃣4️⃣ - mart",
    "15": "1️⃣5️⃣ - mart",
    "16": "1️⃣6️⃣ - mart",
    "17": "1️⃣7️⃣ - mart",
    "18": "1️⃣8️⃣ - mart",
    "19": "1️⃣9️⃣ - mart",
    "20": "2️⃣0️⃣ - mart",
    "21": "2️⃣1️⃣ - mart",
    "22": "2️⃣2️⃣ - mart",
    "23": "2️⃣3️⃣ - mart",
    "24": "2️⃣4️⃣ - mart",
    "25": "2️⃣5️⃣ - mart",
    "26": "2️⃣6️⃣ - mart",
    "27": "2️⃣7️⃣ - mart",
    "28": "2️⃣8️⃣ - mart",
    "29": "2️⃣9️⃣ - mart",
    "30": "1️⃣ - aprel",
    "31": "2️⃣ - aprel",
    "32": "3️⃣ - aprel",
    "33": "4️⃣ - aprel",
    "34": "5️⃣ - aprel",
    "35": "6️⃣ - aprel",
    "36": "7️⃣ - aprel",
    "37": "8️⃣ - aprel",
}


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    context.user_data["days"] = set()

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
    contact = update.message.contact
    phone_number = contact.phone_number
    context.user_data["phone"] = phone_number

    reply_markup = InlineKeyboardMarkup(days_keyboard)

    update.message.reply_text(
        'Ramazonning qaysi kunlarida qatnashmoqchisiz ?\n\n',
        # reply_markup=reply_markup,
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Kunlarni belgilang ?\n\n',
        reply_markup=reply_markup,
    )

    return CHOOSE_PAYMENT


def choose_payment(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    text = update.message.text
    if text == "Naqd":
        update.message.reply_text(
            f'Naqd to`lash so`rovingiz qabul qilindi. Tashakkur ).',
        )
        context.user_data["payment_type"] = "cash"
        user_id = user_id = update.message.from_user.id
        save_data(user_id, context, image=False)
    elif text == "Card":
        update.message.reply_text(
            'Iltimos to`lov chekini rasm ko`rinishida yuboring.'
        )
        context.user_data["payment_type"] = "card"

        return ACCEPT_CHECK

    elif text == "Ortga":
        reply_markup = InlineKeyboardMarkup(days_keyboard)
        days_text = "\n".join(numbers_in_emoji[x] for x in sorted(context.user_data["days"]))

        update.message.reply_text(
            'Ramazonning qaysi kunlarida qatnashmoqchisiz ?\n\n',
            # reply_markup=reply_markup,
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Belgilangan kunlar:\n\n' + days_text,
            reply_markup=reply_markup,
        )

        return CHOOSE_PAYMENT

    return ConversationHandler.END


def accept_check(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    file_id = update.message.photo[-1].file_id
    file_path = context.bot.get_file(file_id).file_path
    context.user_data["payment_check"] = file_path

    user_id = update.message.from_user.id
    save_data(user_id, context, image=True)

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


def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    option_text = "✅ Belgilangan kunlar ?\n\n"
    selected_option = query.data
    reply_markup = InlineKeyboardMarkup(days_keyboard)

    if selected_option == "confirm":
        if len(context.user_data["days"]) == 0:
            query.answer(text="You haven't choose any days", show_alert=True)
        else:
            days = len(context.user_data["days"])
            summa = days * 7000
            keyboard = [['Naqd', 'Card'], ['Ortga']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

            query.message.reply_text(
                f'{days} kun! Jami to`lov {summa} so`m.',
                reply_markup=reply_markup
            )

            return CHOOSE_PAYMENT

    if selected_option != "00" and selected_option != "confirm":
        if selected_option not in context.user_data["days"]:
            context.user_data["days"].add(selected_option)
            text = "\n".join(numbers_in_emoji[x] for x in sorted(context.user_data["days"]))
            query.edit_message_text(text=f"{option_text}{text}", reply_markup=reply_markup)
        else:
            context.user_data["days"].remove(selected_option)
            text = "\n".join(numbers_in_emoji[x] for x in sorted(context.user_data["days"]))
            query.edit_message_text(text=f"{option_text}{text}", reply_markup=reply_markup)


def save_data(user_id, context: CallbackContext, image=False):
    user = User.objects.get(user_id=user_id)
    application = Application.objects.create(
        user=user,
        days=context.user_data["days"],
        phone=context.user_data["phone"],
        payment_type=context.user_data["payment_type"],
    )
    if image:
        file_url = context.user_data["payment_check"]
        response = requests.get(file_url)

        # Save the image to your server
        with open('image.jpg', 'wb') as f:
            f.write(response.content)

        with open('image.jpg', 'rb') as f:
            # Assign the image file to the model's image field
            application.payment_check.save(f'{user}_payment_check.png', File(f))

        # Save the model instance
        application.save()

