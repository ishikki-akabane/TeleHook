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
def start_cmd(client, message):
    name = message.from_user.first_name
    try:
        message.reply_audio("https://alpha.123tokyo.xyz/get.php/e/02/0maE8OVEUtg.mp3?cid=MmEwMTo0Zjg6YzAxMjozMmVlOjoxfE5BfERF&h=Y20nKAnS6D9XbE8uBZFuFw&s=1733648802&n=Tumne%20Humse%20Wada%20Kiya%20Tha%20%28Official%20Video%29%20Munawar%20Faruqui%20ft.%20Nazila%20_%20Saaj%20Bhatt%20_%20SD%20Gana4u&uT=R&uN=aXNoaWtraWFrYWJhbmU%3D")
    except Exception as e:
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')


#@TeleHook.on_edited(Filters.private)
def handle_private_edit(bot, message):
    try:
        message.reply_text(f"Edited message in private chat: {message.text}")
    except Exception as e:
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')


#@TeleHook.on_message(Filters.private)
def read_message1(bot, message):
    try:
        message.reply_text(f"{message.text}")
    except Exception as e:
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')



if __name__ == "__main__":
    app.run()


