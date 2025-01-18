# Methods


from .send_func import SendFunctions
from .callback_func import CallbackFunctions
from .edit_func import EditFunctions

class Methods(
    SendFunctions,
    CallbackFunctions,
    EditFunctions
):
    def __init__(self, client):
        self.client = client
        return

    def test():
        return True
    
    
