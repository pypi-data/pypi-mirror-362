
from torii.data import *
from torii.services.torii_service import ToriiService


class OrganisationService(ToriiService):

    def __init__(self, torii):
        """
        Create the picom service
        """
        ToriiService.__init__(self, torii=torii, name='organisations', object_class=ToriiObject)


    @property
    def local(self):
        """
        Get the local organisation
        :return:
        """

        return ToriiObject(self.request_get('local'))