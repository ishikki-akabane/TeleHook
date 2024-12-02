import requests
from collections import defaultdict
import logging
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeleClient:
    def __init__(self, token: str, webhook_url: str):
        self.token = token
        self.webhook_url = webhook_url
        self.base_url = f'https://api.telegram.org/bot{self.token}'
        self.handlers = defaultdict(list)  # {update_type: [(group, handler)]}

    def set_webhook(self):
        response = requests.post(
            f'{self.base_url}/setWebhook',
            data={'url': self.webhook_url}
        )
        response.raise_for_status()
        logger.info("Webhook set successfully.")

    def _add_handler(self, update_type: str, handler, group: int):
        self.handlers[update_type].append((group, handler))
        self.handlers[update_type].sort(key=lambda x: x[0])  # Sort by group

    def process_update(self, update_data: dict):
        for update_type in update_data:
            if update_type in self.handlers:
                for _, handler in self.handlers[update_type]:
                    stop_processing = handler(update_data[update_type])
                    if stop_processing is not None and stop_processing:
                        break

    def send_message(self, chat_id: int, text: str):
        url = f'{self.base_url}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        response = requests.post(url, json=payload)
        response.raise_for_status()

    def on_message(self, filter_func=None, group=0):
        def decorator(func):
            @wraps(func)
            def wrapper(update_data):
                message = Message(self, update_data)
                if filter_func is None or filter_func(message):
                    return func(self, message)
            self._add_handler('message', wrapper, group)
            return wrapper
        return decorator
        



class Filters:
    @staticmethod
    def command(command: str):
        def filter_func(message):
            return message.text.startswith(f'/{command}')
        return filter_func

