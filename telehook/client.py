import requests
from collections import defaultdict
import logging
from functools import wraps

from telehook.types import *


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
                logger.error(e)
            for handler, filter_ in self.message_handlers:
                if filter_(message):
                    handler(self, message)

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

    def send_message(self, chat_id, text):
        """
        Send a message via the Telegram Bot API.

        Args:
            chat_id (int): The chat ID to send the message to.
            text (str): The text of the message.
        """
        url = self.api_url + "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                logger.info("Failed to send message:", response.text)
        except Exception as e:
            logger.info("Error sending message:", e)
        


class Filters:
    @staticmethod
    def command(command):
        """
        Filter for matching specific bot commands.

        Args:
            command (str): The command to filter for (without the leading slash).

        Returns:
            function: A filter function.
        """
        def filter_func(message):
            if hasattr(message, 'text') and message.text and message.text.startswith(f"/{command}"):
                return True
            return False
        return filter_func

