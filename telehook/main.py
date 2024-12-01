import logging
import requests
from functools import wraps


logger = logging.getLogger('TeleHook')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')



class TeleClient2:
    handlers = []

    @staticmethod
    def on_message(filter_func=None):
        def decorator(func):
            @wraps(func)
            def wrapper(update):
                if filter_func is None or filter_func(update):
                    return func(update)
                return None
            TeleClient2.handlers.append(wrapper)
            return wrapper
        return decorator

    @staticmethod
    def process_update(update):
        for handler in TeleClient2.handlers:
            handler(update)

class Filters:
    @staticmethod
    def command(command):
        def filter_func(update):
            message = update.get('message', {})
            text = message.get('text', '')
            return text.startswith(f'/{command}')
        return filter_func



class TeleClient:
    def __init__(self, token, url):
        self.token = token
        self.url = url
        #self.app = client
        self.status = "Offline"
        self.client_id = None
        self.raw_handler = None
        self.base_url = f'https://api.telegram.org/bot{self.token}'

        # Set the webhook when initializing
        # self.set_webhook()

    def webhook_function(self, update):
        if self.raw_handler:
            self.raw_handler(self.client_id, update)
        return {"ok": True}

    # ====================================================================
    # FILTERS
    def on_raw(self):
        def decorator(func):
            self.raw_handler = func
            return func
        return decorator

    # ====================================================================
    # MISCELLANEOUS
    def set_webhook(self):
        response = requests.post(
            f'{self.base_url}/setWebhook',
            data={'url': self.url}
        )
        self.client_id = response.json()
        if response.status_code == 200:
            self.status = self.client_id
        else:
            self.status = f"Offline - {self.client_id}"
