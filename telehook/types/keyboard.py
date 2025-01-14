from typing import Union, List, Dict, Any


class InlineKeyboardButton:
    def __init__(self, text: str, url: str = None):
        self.text = text
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "url": self.url}


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self) -> Dict[str, Any]:
        return {"inline_keyboard": [[btn.to_dict() for btn in row] for row in self.inline_keyboard]}