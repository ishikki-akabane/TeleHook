

class RPCError(Exception):
    """
    Base class for RPC errors in TeleHook.
    """

    def __init__(self, message, method=None, params=None, code=None):
        self.message = message
        self.method = method
        self.params = params
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        error_message = f"RPCError: {self.message}"
        if self.method:
            error_message += f" (Method: {self.method})"
        if self.code:
            error_message += f" (Code: {self.code})"
        return error_message


class BadRequest(RPCError):
    """
    Raised when the request was malformed or contained invalid data.
    """
    pass


class Unauthorized(RPCError):
    """
    Raised when the bot token is invalid.
    """
    pass


class Forbidden(RPCError):
    """
    Raised when the bot doesn't have permission to perform the requested action.
    """
    pass


class NotFound(RPCError):
    """
    Raised when the requested resource was not found.
    """
    pass


class FloodWait(RPCError):
    """
    Raised when the bot has exceeded rate limits.
    """
    def __init__(self, message, method=None, params=None, code=None, x=None):
        super().__init__(message, method, params, code)
        self.x = x

    def __str__(self):
        return f"{super().__str__()} (Retry after {self.x} seconds)"


class InternalServerError(RPCError):
    """
    Raised when an internal server error occurred on Telegram's side.
    """
    pass
