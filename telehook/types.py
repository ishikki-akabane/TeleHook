# type class

class User:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.first_name = user_data.get('first_name')
        self.last_name = user_data.get('last_name', None)
        self.username = user_data.get('username', None)


class Chat:
    def __init__(self, chat_data):
        self.id = chat_data.get('id')
        self.type = chat_data.get('type')
        self.title = chat_data.get('title')
        self.username = chat_data.get('username', None)


class Message:
    def __init__(self, client, message_data):
        self.client = client
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        #self.chat = Chat(message_data.get('chat', {}))
        #self.from_user = User(message_data.get('from', {}))

    def reply_text(self, text):
        self.client.send_message(7869684136, text)

class Messageee:
    def __init__(self, client, data):
        self.client = client
        self.chat_id = data['chat']['id']
        self.text = data.get('text', '')
        self.from_user = data.get('from', {})

    def reply_text(self, text: str):
        self.client.send_message(chat_id=self.chat_id, text=text)
