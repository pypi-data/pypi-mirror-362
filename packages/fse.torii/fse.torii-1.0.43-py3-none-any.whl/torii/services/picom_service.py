
from torii.exception import ToriiException
from torii.data import *
from torii.services.torii_service import ToriiService


class PicomService(ToriiService):

    def __init__(self, torii):
        """
        Create the picom service
        """
        ToriiService.__init__(self, torii=torii, name='picoms', object_class=Picom)

