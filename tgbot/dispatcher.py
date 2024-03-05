"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    ConversationHandler
)

from dtb.settings import DEBUG
from tgbot.handlers.onboarding.handlers import PAYMENT, CHOOSE_PAYMENT, ACCEPT_CHECK, RAMADANDAYS

from tgbot.handlers.utils import files, error
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
            PAYMENT: [MessageHandler(Filters.regex('^(?:[1-9]|[1-2][0-9])-(?:[2-9]|1\d|30)$'), onboarding_handlers.payment)],
            CHOOSE_PAYMENT: [MessageHandler(Filters.regex('^(Naqd|Card)$'), onboarding_handlers.choose_payment)],
            ACCEPT_CHECK: [MessageHandler(Filters.photo, onboarding_handlers.accept_check)],
        },
        fallbacks=[CommandHandler('cancel', onboarding_handlers.cancel)],
    ))
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)
    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
