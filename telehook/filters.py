# Filters

import inspect


class Filters:
    def __init__(self, func):
        self.func = func

    async def __call__(self, client, message):
        """
        Make Filters callable like Pyrogram's filters.

        Args:
            client: The Telegram client instance.
            message: The message object.

        Returns:
            bool: Whether the filter condition is satisfied.
        """
        if inspect.iscoroutinefunction(self.func):
            return await self.func(client, message)
        else:
            return self.func(client, message)

    def __and__(self, other):
        """
        Combine two filters with AND logic.
        """
        return Filters(lambda client, message: self(client, message) and other(client, message))

    def __or__(self, other):
        """
        Combine two filters with OR logic.
        """
        return Filters(lambda client, message: self(client, message) or other(client, message))

    def __invert__(self):
        """
        Negate a filter with NOT logic.
        """
        return Filters(lambda client, message: not self(client, message))


    @staticmethod
    def command(command):
        """
        Filter for matching specific bot commands.

        Args:
            command (str): The command to filter for (without the leading slash).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            hasattr(message, 'text') and message.text.startswith(f"/{command}"))

    # Use the following filters without calling them
    @staticmethod
    def private():
        """
        Filter for private chats (direct messages).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            getattr(message.chat, "type", None) == "private")

    @staticmethod
    def group():
        """
        Filter for group chats (supergroup or group).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            getattr(message.chat, "type", None) in {"group", "supergroup"})
    
    @staticmethod
    def text():
        return Filters(lambda client, message: bool(getattr(message, 'text', None)))


    @staticmethod
    def photo():
        """
        Filter for messages containing a photo.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'photo', None)))


    @staticmethod
    def video():
        """
        Filter for messages containing a video.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'video', None)))


    @staticmethod
    def audio():
        """
        Filter for messages containing an audio file.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'audio', None)))


    @staticmethod
    def document():
        """
        Filter for messages containing a document.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'document', None)))


    @staticmethod
    def sticker():
        """
        Filter for messages containing a sticker.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'sticker', None)))


    @staticmethod
    def animation():
        """
        Filter for messages containing a sticker.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'animation', None)))


    @staticmethod
    def voice():
        """
        Filter for messages containing a voice message.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'voice', None)))


    @staticmethod
    def caption():
        """
        Filter for messages with a caption.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'caption', None)))


    @staticmethod
    def forwarded():
        """
        Filter for forwarded messages.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'forward_from', None)))


    @staticmethod
    def reply():
        """
        Filter for messages that are replies to other messages.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: bool(getattr(message, 'reply_to_message', None)))


    @staticmethod
    def user(user_id):
        """
        Filter for messages from a specific user.

        Args:
            user_id (int): The user ID to filter for.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: message.from_user and message.from_user.id == user_id)

    @staticmethod
    def chat(chat_id):
        """
        Filter for messages from a specific chat.

        Args:
            chat_id (int): The chat ID to filter for.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: message.chat and message.chat.id == chat_id)

    @staticmethod
    def regex(pattern):
        """
        Filter for messages that match a regex pattern.

        Args:
            pattern (str): The regex pattern to match against.

        Returns:
            Filters: A filter object.
        """
        import re
        return Filters(lambda client, message: message.text and re.search(pattern, message.text))


    @staticmethod
    def all():
        """
        Filter for all chat types.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: True)