import requests
from functools import wraps
import logging

from telehook.types import Message, Chat, User


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
        self.handlers = {
            'message': [],
            'edited_message': [],
            'raw': []
        }

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

   

    def _add_handler(self, update_type: str, filter_func=None):
        def decorator(func):
            @wraps(func)
            def wrapper(update_data):
                if update_type in update_data:
                    message_data = update_data[update_type]
                    message = Message(self, message_data)
                    if filter_func is None or filter_func(message):
                        func(self, message)
            self.handlers[update_type].append((wrapper, filter_func))
            return func
        return decorator

    def on_message(self, filter_func=None):
        return self._add_handler('message', filter_func)

    def on_edited(self, filter_func=None):
        return self._add_handler('edited_message', filter_func)

    def on_raw(self):
        return self._add_handler('raw')

    def process_update(self, update_data: dict):
        for update_type in self.handlers:
            if update_type in update_data:
                for handler, _ in self.handlers[update_type]:
                    handler(update_data)

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
        def filter_func(update):
            message = update.get('message', {})
            text = message.get('text', '')
            return text.startswith(f'/{command}')
        return filter_func
        
