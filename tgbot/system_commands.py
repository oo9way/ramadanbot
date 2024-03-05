from typing import Dict

from telegram import Bot, BotCommand

from tgbot.main import bot


def set_up_commands(bot_instance: Bot) -> None:

    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',

        },
        'es': {
            'start': 'Iniciar el bot de django 🚀',

        },
        'fr': {
            'start': 'Démarrer le bot Django 🚀',

        },
        'ru': {
            'start': 'Запустить django бота 🚀',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


set_up_commands(bot)
