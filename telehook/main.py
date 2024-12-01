import logging
import requests
from functools import wraps


logger = logging.getLogger('TeleHook')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')



class TeleClient:
    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.handlers = {
            'message': [],
            'edited_message': [],
            'raw': []
        }

    def _add_handler(self, update_type, filter_func=None):
        def decorator(func):
            @wraps(func)
            def wrapper(update):
                if update_type == 'raw' or (filter_func and filter_func(update)):
                    func(self, update)
            self.handlers[update_type].append(wrapper)
            return wrapper
        return decorator
        
    def on_message(self, filter_func=None):
        return self._add_handler('message', filter_func)

    def on_edited(self, filter_func=None):
        return self._add_handler('edited_message', filter_func)

    def on_raw(self):
        return self._add_handler('raw')

    def process_update(self, update):
        if 'message' in update:
            for handler in self.handlers['message']:
                handler(update)
        if 'edited_message' in update:
            for handler in self.handlers['edited_message']:
                handler(update)
        for handler in self.handlers['raw']:
            handler(update)

    def send_message(self, chat_id, text):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
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
    def command(command):
        def filter_func(update):
            message = update.get('message', {})
            text = message.get('text', '')
            return text.startswith(f'/{command}')
        return filter_func


class TeleClient2:
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
