# Filters

class Filters:
    @staticmethod
    def command(command):
        """
        Filter for matching specific bot commands.

        Args:
            command (str): The command to filter for (without the leading slash).

        Returns:
            function: A filter function.
        """
        def filter_func(message):
            if hasattr(message, 'text') and message.text and message.text.startswith(f"/{command}"):
                return True
            return False
        return filter_func

    @staticmethod
    def private(message):
        """
        Filter for private chats (direct messages).

        Args:
            message: The message object.

        Returns:
            bool: True if the message is from a private chat.
        """
        return getattr(message.chat, "type", None) == "private"

    @staticmethod
    def group(message):
        """
        Filter for group chats (supergroup or group).

        Args:
            message: The message object.

        Returns:
            bool: True if the message is from a group or supergroup.
        """
        return getattr(message.chat, "type", None) in {"group", "supergroup"}

    @staticmethod
    def all(message):
        """
        Filter for all chat types.

        Args:
            message: The message object.

        Returns:
            bool: Always True.
        """
        return True
