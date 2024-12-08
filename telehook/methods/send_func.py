
#from telehook.client import logger
import requests


class send_func:
    def send_message(self, chat_id, text):
        """
        Send a message via the Telegram Bot API.

        Args:
            chat_id (int): The chat ID to send the message to.
            text (str): The text of the message.
        """
        url = self.client.api_url + "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                return
        except Exception as e:
            return

    def send_audio(self, chat_id, audio_path, filename="audio.mp3"):
        """
        Send an audio file via the Telegram Bot API.

        Args:
            chat_id (int): The chat ID to send the audio to.
            audio_content (bytes): The content of the audio file.
            filename (str): The name of the file to be sent.
        """
        url = self.client.api_url + "sendAudio"
