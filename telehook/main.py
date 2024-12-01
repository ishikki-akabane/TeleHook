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
        self.handlers = {}

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

   

    def add_handler(self, update_type, func, filter_func=None):
        if update_type not in self.handlers:
            self.handlers[update_type] = []
        self.handlers[update_type].append({"handler": func, "filter": filter_func})

    def on_message(self, filter_func=None):
        def decorator(func):
            self.add_handler('message', func, filter_func)
            return func
        return decorator

    def on_edited(self, filter_func=None):
        def decorator(func):
            self.add_handler('edited_message', func, filter_func)
            return func
        return decorator

    def process_update(self, update_data: dict):
        for update_type, handlers in self.handlers.items():
            if update_type in update_data:
                for handler_obj in handlers:
                    handler = handler_obj["handler"]
                    filter_func = handler_obj["filter"]
                    message_data = update_data[update_type]
                    message = Message(self, message_data)
                    if not filter_func or filter_func(message):
                        try:
                            handler(self, message)
                        except Exception as e:
                            logger.error(f"Error in handler {handler.__name__}: {e}")

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
        
