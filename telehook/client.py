

import requests
import logging

from telehook.types import Message
from telehook.filters import Filters
from telehook.methods import Methods


BOT_TOKEN = "7612816971:AAFeh2njq6BcCEi-xTN5bLE7qKnAnzvvHMY"
CHAT_ID = 7869684136


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeleClient:
    def __init__(self, token, url=None):
        """
        Initialize the TeleClient.

        Args:
            token (str): Telegram Bot API token.
            url (str): Optional webhook URL for the bot.
        """
        self.token = token
        self.url = url
        self.api_url = f"https://api.telegram.org/bot{self.token}/"
        self.message_handlers = []
        self.edited_message_handlers = []
        self.method = Methods(self)

    def process_update(self, update):
        """
        Process an incoming update.

        Args:
            update (dict): The Telegram webhook update.
        """
        if "message" in update:
            try:
                message = Message(self, update["message"])
            except Exception as e:
                requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')
            for handler, filter_ in self.message_handlers:
                if filter_(message):
                    handler(self, message)

        elif "edited_message" in update:
            try:
                edited_message = Message(self, update["edited_message"])
            except Exception as e:
                requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')
            for handler, filter_ in self.edited_message_handlers:
                if filter_(edited_message):
                    handler(self, edited_message)

    def on_message(self, filter_func):
        """
        Decorator to handle messages with a specific filter.

        Args:
            filter_func (function): A function that determines whether the handler should be called.

        Returns:
            function: The decorated function.
        """
        def decorator(func):
            self.message_handlers.append((func, filter_func))
            return func
        return decorator

    def on_edited(self, filter_func):
        """
        Decorator to handle edited messages with a specific filter.

        Args:
            filter_func (function): A function that determines whether the handler should be called.

        Returns:
            function: The decorated function.
        """
        def decorator(func):
            self.edited_message_handlers.append((func, filter_func))
            return func
        return decorator

