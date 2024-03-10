"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    ConversationHandler, CallbackQueryHandler
)

from dtb.settings import DEBUG
from tgbot.handlers.onboarding.handlers import CHOOSE_PAYMENT, ACCEPT_CHECK, RAMADANDAYS, button_click, \
    WAITING_FOR_IMAGE, request_image_again, accept_check, CHOOSE_ORDER_TYPE, PHONE2, command_info,command_prayertimes

from tgbot.handlers.utils import error
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.main import bot


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', onboarding_handlers.command_start)],
        states={
            RAMADANDAYS: [MessageHandler(Filters.contact, onboarding_handlers.ramadan_days)],
            PHONE2: [
                MessageHandler(Filters.regex('^(Skip|[-+]?[0-9]+)$'), onboarding_handlers.phone_second)],

            CHOOSE_ORDER_TYPE: [MessageHandler(Filters.regex('^(Onsite|Take away|Back)$'), onboarding_handlers.choose_order_type)],
            CHOOSE_PAYMENT: [MessageHandler(Filters.regex('^(Cash|Card|Back)$'), onboarding_handlers.choose_payment)],
            WAITING_FOR_IMAGE: [
            MessageHandler(Filters.photo, accept_check),
            MessageHandler(Filters.text & (~Filters.command), request_image_again),
        ],
            ACCEPT_CHECK: [MessageHandler(Filters.photo, onboarding_handlers.accept_check)],
        },
        fallbacks=[CommandHandler('cancel', onboarding_handlers.cancel)],
    ))

    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(CommandHandler('info', command_info))
    dp.add_handler(CommandHandler('prayertimes', command_prayertimes))

    dp.add_error_handler(error.send_stacktrace_to_tg_chat)
    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
