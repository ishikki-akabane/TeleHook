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
    def private():
        """
        Filter for private chats (direct messages).

        Returns:
            function: A filter function.
        """
        def filter_func(message):
            return getattr(message.chat, "type", None) == "private"
        return filter_func

    @staticmethod
    def group(message):
        """
        Filter for group chats (supergroup or group).

        Returns:
            function: A filter function.
        """
        """
        def filter_func(message):
            return getattr(message.chat, "type", None) in {"group", "supergroup"}
        return filter_func
        """
        return getattr(message.chat, "type", None) in {"group", "supergroup"}

    @staticmethod
    def all():
        """
        Filter for all chat types.

        Returns:
            function: A filter function.
        """
        def filter_func(message):
            return True
        return filter_func
