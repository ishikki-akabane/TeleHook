
import requests
import httpx
from typing import Union, Optional
import json


class CallbackFunctions:
    async def answer_callback_query(
            self,
            callback_query_id,
            text=None,
            show_alert=False,
            url=None,
            cache_time=0
        ):
        """
        Answer a callback query.
        """
        payload = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time
        }
        url = f"{self.client.api_url}answerCallbackQuery"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()