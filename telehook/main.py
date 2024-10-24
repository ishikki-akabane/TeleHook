

import logging
import requests
import aiohttp


logger = logging.getLogger('TeleHook')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TeleClient:
    """
    The main class for interacting with GramDB, providing methods for authentication, data manipulation, and background tasks.
    """
    def __init__(self):
        print("started")
