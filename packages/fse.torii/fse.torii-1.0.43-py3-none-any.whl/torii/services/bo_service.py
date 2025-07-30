
from torii.data import *
from torii.services.torii_service import ToriiService


class BusinessObjectService(ToriiService):

    def __init__(self, torii, bo_name, object_class=BusinessObject):
        """
        Create the BO service

        :param torii:
        :param bo_name:
        """
        ToriiService.__init__(self, torii=torii, name='bo/{0}'.format(bo_name), object_class=object_class)
