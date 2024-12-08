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
        text = f"```json\n{update}\n```"
        #requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown')
        TeleHook.process_update(update)
    except Exception as e:
        text = f"```python\nException: {e}\n```"

    return 'ok'

# ====================================================================

@TeleHook.on_message(Filters.command('start'))
def start_cmd(client, message):
    name = message.from_user.first_name
    output_path = "music.mp3"
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    """
    download_link = message.text.split(None, 1)[1]
    response = requests.get(download_link, stream=True)
    """
    try:
        message.reply_audio(output_path) #, {user_info}")
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


