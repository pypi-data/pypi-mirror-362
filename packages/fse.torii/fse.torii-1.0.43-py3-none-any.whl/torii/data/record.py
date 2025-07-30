
from torii.data.struct import Struct

class Record(Struct):
    """
    Wrapper for the task records
    """

    def __init__(self, json={}, service=None):
        Struct.__init__(self, json)

        self._service = service
