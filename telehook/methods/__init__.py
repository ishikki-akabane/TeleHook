# Methods


from .send_func import SendFunctions
from .callback_func import CallbackFunctions


class Methods(
    SendFunctions,
    CallbackFunctions
):
    def __init__(self, client):
        self.client = client
        return

    def test():
        return True
    
    
