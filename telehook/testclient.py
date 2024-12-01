from flask import Flask, request
import requests

class testclient:
    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.app = Flask(__name__)
        self.status = "Offline"
        self.client_id = None
        self.raw_handler = None
        self.base_url = f'https://api.telegram.org/bot{self.token}'

        self.app.add_url_rule("/", view_func=self.home_endpoint, methods=["GET"])
        self.app.add_url_rule("/status", view_func=self.status_endpoint, methods=["GET"])
        self.app.add_url_rule("/webhook", view_func=self.webhook_endpoint, methods=["POST"])
        
        # Set the webhook when initializing
        self.set_webhook()

    def home_endpoint(self):
        return "Telegram Webhook is running."

    def status_endpoint(self):
        return jsonify({"status": self.status, "webhook_url": self.url})

    def webhook_endpoint(self):
        update = request.json
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
            
    def run(self):
        self.app.run()
