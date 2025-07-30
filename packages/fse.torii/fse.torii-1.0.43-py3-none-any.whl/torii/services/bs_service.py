
from torii.data import *
from torii.services.torii_service import ToriiService


class BSService(ToriiService):

    def __init__(self, torii):
        """
        Create the BO service

        :param torii:
        :param bo_name:
        """
        ToriiService.__init__(self, torii=torii, name='pythonServices', object_class=ToriiObject)

    def tail(self, bs, limit=100):
        """
        Start a business service

        :param bs: the business service
        :return:
        """

        json = self.request('GET', path='{0}/tail'.format(bs.id), params={'limit': limit},)
        bs.from_json(json)

        return bs

    def start(self, bs):
        """
        Start a business service

        :param bs: the business service
        :return:
        """

        json = self.request('GET', path='{0}/start'.format(bs.id))
        bs.from_json(json)

        return bs

    def stop(self, bs):
        """
        Stop a business service

        :param bs: the business service
        :return:
        """

        json = self.request('GET', path='{0}/stop'.format(bs.id))
        bs.from_json(json)

        return bs

    def restart(self, bs):
        """
        Restart a business service

        :param bs: the business service
        :return:
        """

        json = self.request('GET', path='{0}/restart'.format(bs.id))
        bs.from_json(json)

        return bs

    def status(self, bs=None):
        """
        Get the status of one/all business service

        :param bs: the business service(s)
        :return:
        """

        if bs:
            json = self.request('GET', path='{0}/status'.format(bs.id))
            bs.from_json(json)

            return bs
        else:
            json = self.request('GET', path='status')

            bss = [self._object_class(x, service=self) for x in json]
            return bss
