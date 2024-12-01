# testing 
"""
from telehook import TeleClient, Filters


app = TeleClient(
    token="7381276983:AAF9uBsYozCj8B2_J9jwkPUj_ohDFmNPXic",
    webhook_url="https://test-drive-555.vercel.app/"
)



def send_message(client, chat_id, text):
    url = f"https://api.telegram.org/bot{client.token}/sendMessage"
    httpx.post(url, data={"chat_id": chat_id, "text": text})



@app.on_message(Filters.command("start"))
async def start_cmd(client, message):
    chat_id = message['chat']['id']
    send_message(client, chat_id, "started")


print("started...")
app.run()
"""


from flask import Flask, request, jsonify
import requests
from telehook import TeleClient


BOT_TOKEN = "7612816971:AAFeh2njq6BcCEi-xTN5bLE7qKnAnzvvHMY"
CHAT_ID = 7869684136


app = Flask(__name__)
TeleHook = TeleClient(
    token=BOT_TOKEN,
    url='https://telehook-test.vercel.app/webhook',
    client=app
)

@app.route("/")
def home_endpoint():
    return "Telegram Webhook is running."

@app.route('/webhook', methods=['POST'])
def webhook_endpoint():
    try:
        update = request.json
        text = f"```python\n{update}\n```"
    except Exception as e:
        text = f"```python\n{e}\n```"

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown'
    response = requests.get(url)
    #TeleHook.webhook_function(update)
    return 'ok'

@app.route("/status")
def status_endpoint():
    return f"Status: {TeleHook.status}"



# ====================================================================

#@TeleHook.on_raw()
def get_raw_update(client, message):
    text = f"```python\nClient ID: {client}\nMessage: {message}\n```"
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown'
    response = requests.get(url)





