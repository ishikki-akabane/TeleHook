from typing import Union, List, Dict, Any


class InlineKeyboardButton:
    def __init__(self, text: str, callback_data: str = None, url: str = None):
        self.text = text
        self.callback_data = callback_data
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        button_dict = {"text": self.text}
        if self.callback_data:
            button_dict["callback_data"] = self.callback_data
        if self.url:
            button_dict["url"] = self.url
        return button_dict


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self) -> Dict[str, Any]:
        return {"inline_keyboard": [[btn.to_dict() for btn in row] for row in self.inline_keyboard]}