# Message

from telehook.types.user import User
from telehook.types.chat import Chat

class Message:
    def __init__(self, client, message_data):
        self.client = client
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        self.chat = Chat(message_data.get('chat', {}))
        self.from_user = User(message_data.get('from', {}))
        self.photo = message_data.get('photo')
        self.caption = message_data.get('caption')
        self.video = message_data.get('video')
        self.audio = message_data.get('audio')
        self.document = message_data.get('document')
        self.sticker = message_data.get('sticker')
        self.animation = message_data.get('animation')
        self.voice = message_data.get('voice')

    async def reply_text(self, text):
        """
        Sends a reply message to the same chat.

        Args:
            text (str): The text of the reply message.
        """
        await self.client.method.send_message(chat_id=self.chat.id, text=text)

    def reply_audio(self, audio):
        """
        Sends a reply message to the same chat.

        Args:
            text (str): The text of the reply message.
        """
        self.client.method.send_audio(chat_id=self.chat.id, audio=audio)
        


class EditedMessage:
    def __init__(self, client, message_data):
        self.client = client
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        self.chat = Chat(message_data.get('chat', {}))
        self.from_user = User(message_data.get('from', {}))

    def reply_text(self, text):
        """
        Sends a reply message to the same chat.

        Args:
            text (str): The text of the reply message.
        """
        self.client.method.send_message(chat_id=self.chat.id, text=text)
