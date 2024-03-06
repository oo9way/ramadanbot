import os
import requests
from django.core.files import File
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from users.models import User, Application
import logging
from datetime import datetime
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

RAMADANDAYS, PAYMENT, LOCATION, ACCEPT_CHECK, CHOOSE_PAYMENT, CASH, CARD = range(7)
WAITING_FOR_IMAGE = 8
days_keyboard = [
    [
        InlineKeyboardButton("March", callback_data="00"),
    ],
    [
        InlineKeyboardButton("11", callback_data='2024-03-11'),
        InlineKeyboardButton("12", callback_data='2024-03-12'),
        InlineKeyboardButton("13", callback_data='2024-03-13'),
        InlineKeyboardButton("14", callback_data='2024-03-14'),
        InlineKeyboardButton("15", callback_data='2024-03-15'),
        InlineKeyboardButton("16", callback_data='2024-03-16'),
        InlineKeyboardButton("17", callback_data='2024-03-17'),
    ],
    [
        InlineKeyboardButton("18", callback_data='2024-03-18'),
        InlineKeyboardButton("19", callback_data='2024-03-19'),
        InlineKeyboardButton("20", callback_data='2024-03-20'),
        InlineKeyboardButton("21", callback_data='2024-03-21'),
        InlineKeyboardButton("22", callback_data='2024-03-22'),
        InlineKeyboardButton("23", callback_data='2024-03-23'),
        InlineKeyboardButton("24", callback_data='2024-03-24'),
        InlineKeyboardButton("25", callback_data='2024-03-25'),
    ],
    [
        InlineKeyboardButton("26", callback_data='2024-03-26'),
        InlineKeyboardButton("27", callback_data='2024-03-27'),
        InlineKeyboardButton("28", callback_data='2024-03-28'),
        InlineKeyboardButton("29", callback_data='2024-03-29'),
        InlineKeyboardButton("30", callback_data='2024-03-30'),
        InlineKeyboardButton("31", callback_data='2024-03-31'),
        InlineKeyboardButton("*", callback_data='00'),
        InlineKeyboardButton("*", callback_data='00'),
    ],
    [
        InlineKeyboardButton("April", callback_data="00"),
    ],
    [
        InlineKeyboardButton("1", callback_data='2024-04-01'),
        InlineKeyboardButton("2", callback_data='2024-04-02'),
        InlineKeyboardButton("3", callback_data='2024-04-03'),
        InlineKeyboardButton("4", callback_data='2024-04-04'),
        InlineKeyboardButton("5", callback_data='2024-04-05'),
        InlineKeyboardButton("6", callback_data='2024-04-06'),
        InlineKeyboardButton("7", callback_data='2024-04-07'),
        InlineKeyboardButton("8", callback_data='2024-04-08'),
    ],
    [
        InlineKeyboardButton("9", callback_data='2024-04-09'),
        InlineKeyboardButton("Select All", callback_data="select_all"),
    ],
    [
        InlineKeyboardButton("Confirm", callback_data="confirm"),
    ]
]

numbers_in_emoji = {
    "2024-03-11": "1️⃣1️⃣ - March",
    "2024-03-12": "1️⃣2️⃣ - March",
    "2024-03-13": "1️⃣3️⃣ - March",
    "2024-03-14": "1️⃣4️⃣ - March",
    "2024-03-15": "1️⃣5️⃣ - March",
    "2024-03-16": "1️⃣6️⃣ - March",
    "2024-03-17": "1️⃣7️⃣ - March",
    "2024-03-18": "1️⃣8️⃣ - March",
    "2024-03-19": "1️⃣9️⃣ - March",
    "2024-03-20": "2️⃣0️⃣ - March",
    "2024-03-21": "2️⃣1️⃣ - March",
    "2024-03-22": "2️⃣2️⃣ - March",
    "2024-03-23": "2️⃣3️⃣ - March",
    "2024-03-24": "2️⃣4️⃣ - March",
    "2024-03-25": "2️⃣5️⃣ - March",
    "2024-03-26": "2️⃣6️⃣ - March",
    "2024-03-27": "2️⃣7️⃣ - March",
    "2024-03-28": "2️⃣8️⃣ - March",
    "2024-03-29": "2️⃣9️⃣ - March",
    "2024-03-30": "3️⃣0️⃣ - March",
    "2024-03-31": "3️⃣1️⃣ - March",
    "2024-04-01": "1️⃣ - April",
    "2024-04-02": "2️⃣ - April",
    "2024-04-03": "3️⃣ - April",
    "2024-04-04": "4️⃣ - April",
    "2024-04-05": "5️⃣ - April",
    "2024-04-06": "6️⃣ - April",
    "2024-04-07": "7️⃣ - April",
    "2024-04-08": "8️⃣ - April",
    "2024-04-09": "9️⃣ - April",
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
        f"\nSend your phone number ",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Share your phone number",request_contact=True, )]],
            resize_keyboard=True,
        ))

    return RAMADANDAYS


def ramadan_days(update: Update, context: CallbackContext) -> int:
    contact = update.message.contact
    phone_number = contact.phone_number
    context.user_data["phone"] = phone_number

    reply_markup = InlineKeyboardMarkup(days_keyboard)

    update.message.reply_text(
        'Which days you want to attend for Iftar?\n\n',
        # reply_markup=reply_markup,
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        '🗓 Select days\n\n',
        reply_markup=reply_markup,
    )

    return CHOOSE_PAYMENT

bank_account_details = """
Bank Name: <strong>Keb Hana Bank(하나은행)</strong>
Account Name: <b>Mukammadaliev Bekhzodbek</b>
Account Number: <code>74891124393407</code>.

Please send the screenshot of the payment you made through online banking.
"""

def choose_payment(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    text = update.message.text
    if text == "Cash":
        update.message.reply_text(
            f"""
You've chosen to make a cash payment. Kindly ensure the payment is completed by 2:00 PM, 
as the Iftar arrangements will be prepared based on the number of people who have paid by that time.

Connect with the admin for the payment:
Name: Mukammadaliev Bekhzodbek
Phone: +821039212299

Please note: Bring exact cash to avoid the need for change or currency exchange.. ✨🌙
""",
)
        context.user_data["payment_type"] = "cash"
        user_id = user_id = update.message.from_user.id
        save_data(user_id, context, image=False)
    elif text == "Card":
        update.message.reply_text(
            "Please send a screenshot of your payment. Ensure it is clear and shows the necessary transaction details.",
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        context.user_data["payment_type"] = "card"
        return WAITING_FOR_IMAGE  # Return the new state to wait for the image

    elif text == "Back":
        reply_markup = InlineKeyboardMarkup(days_keyboard)
        days_text = "\n".join(numbers_in_emoji[x] for x in sorted(context.user_data["days"]))

        update.message.reply_text(
            'Which days you want to attend for Iftar ?\n\n',
            # reply_markup=reply_markup,
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            '🗓 Selected days:\n\n' + days_text,
            reply_markup=reply_markup,
        )

        return CHOOSE_PAYMENT

    return ConversationHandler.END


def accept_check(update: Update, context: CallbackContext) -> int:
    file_id = update.message.photo[-1].file_id
    file_path = context.bot.get_file(file_id).file_path
    context.user_data["payment_check"] = file_path
    
    user_id = update.message.from_user.id
    save_data(user_id, context, image=True)
    
    if "days" in context.user_data and context.user_data["days"]:
        # Sort the days
        sorted_days = sorted(context.user_data["days"])
        # Convert each day into the desired format (without emojis for numbers, but you could add content emojis)
        formatted_days = [f"{datetime.strptime(day, '%Y-%m-%d').strftime('%d-%B')}" for day in sorted_days]
        # Organize the formatted days into three columns
        columns = [" | ".join(formatted_days[i:i+3]) for i in range(0, len(formatted_days), 3)]
        selected_days = '\n'.join(columns)
    else:
        selected_days = "No days selected. Please ensure your selection was made correctly."

    update.message.reply_text(
        f"""
Your request has been received. Thank you {update.message.from_user.first_name}!
Here are the days you've chosen: 
{selected_days}

Status: Pending 🕒✨🌙✨🌙✨🌙
""",
    )

    return ConversationHandler.END

def request_image_again(update: Update, context: CallbackContext) -> int:
    """Prompts the user to send an image if they send text instead."""
    update.message.reply_text("Please send a screenshot of the payment. We need an image to verify the transaction.")
    return WAITING_FOR_IMAGE

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
    option_text = "✅ Selected days\n\n"
    selected_option = query.data
    reply_markup = InlineKeyboardMarkup(days_keyboard)

    # Initialize "days" as a set if not already done
    if "days" not in context.user_data:
        context.user_data["days"] = set()

    if selected_option == "confirm":
        if not context.user_data["days"]:
            query.answer(text="You haven't chosen any days", show_alert=True)
        else:
            days = len(context.user_data["days"])
            summa = days * 7000
            keyboard = [['Cash', 'Card'], ['Back']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

            query.message.reply_text(
                f'{days} days! Total {summa} won.',
                reply_markup=reply_markup
            )

            return CHOOSE_PAYMENT

    elif selected_option == "select_all":
        all_days = ['2024-03-11', '2024-03-12', '2024-03-13', '2024-03-14', '2024-03-15',
                    '2024-03-16', '2024-03-17', '2024-03-18', '2024-03-19', '2024-03-20',
                    '2024-03-21', '2024-03-22', '2024-03-23', '2024-03-24', '2024-03-25',
                    '2024-03-26', '2024-03-27', '2024-03-28', '2024-03-29', '2024-03-30',
                    '2024-03-31', '2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04',
                    '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
        context.user_data["days"] = set(all_days)
        query.answer(text="All days have been selected.")

        text = "\n".join(numbers_in_emoji[day] for day in sorted(context.user_data["days"]))
        query.edit_message_text(text=f"{option_text}{text}", reply_markup=reply_markup)

    elif selected_option not in ["00", "confirm", "select_all"]:  # Handle day selections
        if selected_option in context.user_data["days"]:
            context.user_data["days"].remove(selected_option)
        else:
            context.user_data["days"].add(selected_option)

        if context.user_data["days"]:  # Ensure there are selected days to display
            text = "\n".join(numbers_in_emoji[x] for x in sorted(context.user_data["days"]))
        else:
            text = "No days selected."

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

