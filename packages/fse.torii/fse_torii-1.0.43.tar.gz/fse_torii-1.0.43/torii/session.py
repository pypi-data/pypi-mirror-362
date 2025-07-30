from time import time

from requests import Session
from requests.adapters import HTTPAdapter


class CustomSession(Session):

    def __init__(self):
        super().__init__()
        self.t = time()

    def reset_connection(self):
        self.close()
        adapter = HTTPAdapter()
        self.mount('https://', adapter)
        self.mount('http://', adapter)

    def request(self, *args, **kwargs):
        # If it has been more than 4 minutes since last request
        if (time() - self.t) >= 240:
            self.reset_connection()
        self.t = time()

        response = super().request(*args, **kwargs)
        response.raise_for_status()

        return response
