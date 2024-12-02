import requests
from functools import wraps
import logging
from collections import defaultdict

from telehook.types import Message, Chat, User

BOT_TOKEN = "7612816971:AAFeh2njq6BcCEi-xTN5bLE7qKnAnzvvHMY"
CHAT_ID = 7869684136


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TeleClient:
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        self.base_url = f'https://api.telegram.org/bot{self.token}'
        self.handlers = defaultdict(list) # {update_type: [(group, handler, filter)]}

    def connect_webhook(self):
        try:
            response = requests.post(
                f'{self.base_url}/setWebhook',
                data={'url': self.url}
            )
            response.raise_for_status()
            return "Webhook connected successfully."
        except requests.exceptions.RequestException as e:
            return f"Failed to connect webhook: {e}"
   

    def _add_handler(self, update_type: str, filter_func=None, group: int = 0):
        """
        Register a new handler for a specific update type.
        """
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=step1')
        def decorator(func):
            @wraps(func)
            def wrapper(update_data):
                message_data = update_data.get(update_type, {})
                message = Message(self, message_data)
                if filter_func is None or filter_func(message):
                    return func(self, message)
            self.handlers[update_type].append((group, wrapper))
            self.handlers[update_type].sort(key=lambda x: x[0])  # Sort by group
            return func
        return decorator

    def on_message(self, filter_func=None, group: int = 0):
        return self._add_handler('message', filter_func, group)

    def on_edited_message(self, filter_func=None, group: int = 0):
        return self._add_handler('edited_message', filter_func, group)

    def on_raw(self, group: int = 0):
        return self._add_handler('raw', None, group)

    def process_update(self, update_data: dict):
        """
        Process incoming updates and trigger the appropriate handlers.
        """
        for update_type, handlers in self.handlers.items():
            if update_type in update_data:
                for _, handler in handlers:
                    stop_processing = handler(update_data)
                    if stop_processing is not None and stop_processing:
                        # Stop processing further handlers for this update type
                        break

    
    def send_message(self, chat_id: int, text: str):
        url = f'{self.base_url}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info("Message sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message: {e}")


class Filters:
    @staticmethod
    def command(command: str):
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=step2')
        def filter_func(update):
            message = update.get('message', {})
            text = message.get('text', '')
            return text.startswith(f'/{command}')
        return filter_func
        
