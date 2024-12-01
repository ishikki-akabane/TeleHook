from flask import Flask, request, jsonify
import requests

class testclient:
    def __init__(self, token, url, client):
        self.token = token
        self.url = url
        self.app = client
        self.status = "Offline"
        self.client_id = None
        self.raw_handler = None
        self.base_url = f'https://api.telegram.org/bot{self.token}'

        # Set the webhook when initializing
        self.set_webhook()

    def webhook_function(self, update):
        if self.raw_handler:
            self.raw_handler(self.client_id, update)
        return jsonify({"ok": True})

    # ====================================================================
    def on_raw(self):
        def decorator(func):
            self.raw_handler = func
            return func
        return decorator

    # ====================================================================
    def set_webhook(self):
        response = requests.post(
            f'{self.base_url}/setWebhook',
            data={'url': self.url}
        )
        self.client_id = response.json()
        if response.status_code == 200:
            self.status = "Online"
        else:
            self.status = f"Offline - {self.client_id}"
