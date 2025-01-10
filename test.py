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
async def webhook_endpoint():
    try:
        update = request.get_json()
        await TeleHook.process_update(update)
    except Exception as e:
        print(e)

    return 'ok'

# ====================================================================

@TeleHook.on_message(Filters.command('start'))
async def start_cmd(client, message):
    name = message.from_user.first_name
    try:
        await message.reply_text("hellooo")
    except Exception as e:
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')




if __name__ == "__main__":
    app.run()


