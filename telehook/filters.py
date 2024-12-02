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
