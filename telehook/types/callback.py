from typing import Optional, List, Union
from telehook.types.user import User
from telehook.types.chat import Chat
from telehook.types.message import Message


class CallbackQuery:
    def __init__(self, client, data):
        #print(data)
        self.client = client
        self.id = data.get("id")
        self.from_user = User(data.get("from"))
        self.message = Message(client, data.get("message")) if data.get("message") else None
        self.inline_message_id = data.get("inline_message_id")
        self.chat_instance = data.get("chat_instance")
        self.data = data.get("data")
        self.game_short_name = data.get("game_short_name")

    async def answer(self, text=None, show_alert=False, url=None, cache_time=0):
        """
        Answer the callback query.
        """
        return await self.client.method.answer_callback_query(
            self.id, text, show_alert, url, cache_time
        )