import requests
import httpx
from typing import Union, Optional
from ..types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import json


class EditFunctions:
    async def edit_message_text(
        self,
        chat_id: Union[int, str],
        message_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: InlineKeyboardMarkup = None
    ):
        """
        Edit the text of a message.

        Args:
            chat_id (Union[int, str]): Unique identifier for the target chat or username of the target channel.
            message_id (int): Identifier of the message to edit.
            text (str): New text of the message, 1-4096 characters after entities parsing.
            parse_mode (Optional[str]): Mode for parsing entities in the message text.
            reply_markup (Optional[InlineKeyboardMarkup]): A JSON-serialized object for an inline keyboard.

        Returns:
            Message: On success, the edited Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        url = f"{self.client.api_url}editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }

        # Add optional parameters if they are provided
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup.to_dict())

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return Message(self.client, response.json()["result"])
        except Exception as e:
            print(f"Error editing message: {e}")

