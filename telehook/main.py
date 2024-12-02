import requests
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeleClient:
    def __init__(self, token: str, url: str):
        self.token = token
        self.webhook_url = url
        self.base_url = f'https://api.telegram.org/bot{self.token}'
        self.handlers = defaultdict(list)  # {update_type: [handler]}

    def set_webhook(self):
        response = requests.post(
            f'{self.base_url}/setWebhook',
            data={'url': self.webhook_url}
        )
        return response.json()

    def add_handler(self, update_type: str, handler):
        self.handlers[update_type].append(handler)

    def process_update(self, update_data: dict):
        for update_type in update_data:
            if update_type in self.handlers:
                for handler in self.handlers[update_type]:
                    handler(Message(update_data[update_type]))

    def send_message(self, chat_id: int, text: str):
        url = f'{self.base_url}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        response = requests.post(url, json=payload)
        return response.json()


def on_message(client):
    def decorator(func):
        client.add_handler('message', func)
        return func
    return decorator


class Filters:
    @staticmethod
    def command(command: str):
        def filter_func(message):
            return message.text.startswith(f'/{command}')
        return filter_func


class Message:
    def __init__(self, data):
        self.chat_id = data['chat']['id']
        self.text = data.get('text', '')
