# testing


from flask import Flask, request, jsonify
import requests
from telehook import TeleClient, Filters


BOT_TOKEN = "7612816971:AAFeh2njq6BcCEi-xTN5bLE7qKnAnzvvHMY"
CHAT_ID = 7869684136

app = Flask(__name__)
TeleHook = TeleClient(
    token=BOT_TOKEN,
    url='https://telehook-test.vercel.app/webhook'
)

@app.route("/")
def home_endpoint():
    return "Telegram Webhook is running."

@app.route('/webhook', methods=['POST'])
def webhook_endpoint():
    try:
        update = request.get_json()
        text = f"{update}"
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}')
        TeleHook.process_update(update)
    except Exception as e:
        text = f"```python\nException: {e}\n```"

    return 'ok'
    """
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={str(e)}'
        response = requests.get(url)

    return 'ok'
    """



# ====================================================================

@TeleHook.on_message(Filters.command('start'))
def start_cmd(client, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    user_info = message.from_user
    message.reply_text(f"hola, {user_info}")





