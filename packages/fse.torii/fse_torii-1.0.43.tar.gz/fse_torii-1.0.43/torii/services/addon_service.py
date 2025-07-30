import sys
import zipfile

from torii.exception import ToriiException
from torii.data import *
from torii.services.torii_service import ToriiService


class AddonService(ToriiService):

    def __init__(self, torii):
        """
        Create the addon service
        """
        ToriiService.__init__(self, torii=torii, name='addons', object_class=ToriiObject)

    def add(self, path):
        """
        Add an addon to Gateway

        :param path: path to the zip file of the addon
        :return: the addon
        """
        if not zipfile.is_zipfile(path):
            raise ToriiException('Failed to add addon. Bad ZIP file: {0}.'.format(path))
        with open(path, 'rb') as fd:
            try:
                r = self._torii.http_session.request(method='POST',
                                                     headers={'Content-Type': 'application/octet-stream'},
                                                     url=self.get_url('add'),
                                                     stream=True,
                                                     data=fd)
                if r.status_code not in [200, 204]:
                    raise ToriiException('Failed to add addon from {0} (code = {1}) \n{2}'
                                         .format(path, r.status_code, r.reason))
                # content =
                # content = json_lib.loads(content)
                # addon = ToriiObject(json=content, service=self)

                return r.json()

            except ToriiException:
                raise
            except Exception as e:
                raise ToriiException('Failed to add addon from {0} \n{1}'
                                     .format(path, e)).with_traceback(sys.exc_info()[2])

    def _updatezip(self, uuid, path):
        """
        Update an existing addon
        :param uuid: identifier of addon
        :param path: path to the zip file of the addon
        :return: the updated addon
        """
        with open(path, 'rb') as fd:
            try:
                r = self._torii.http_session.request(method='POST',
                                                     headers={'Content-Type': 'application/octet-stream'},
                                                     url=self.get_url('{0}/updateZip'.format(uuid)),
                                                     stream=True,
                                                     data=fd)
                if r.status_code not in [200, 204]:
                    raise ToriiException('Failed to update addon from {0} (code = {1}) \n{2}'
                                         .format(path, r.status_code, r.reason))

                return r.json()

            except ToriiException:
                raise
            except Exception as e:
                raise ToriiException('Failed to update addon from {0} \n{1}'
                                     .format(path, e)).with_traceback(sys.exc_info()[2])

    def update(self, addon, create=False, **kwargs):
        """
        Update an existing addon
        :param addon: the addon
        :param create: False
        :param kwargs: extra parameters (zip=path)
        :return: the updated addon
        """

        # Search fields:
        if kwargs:
            for key, value in kwargs.items():
                # Set field: zip
                if key == 'zip':
                    if not zipfile.is_zipfile(value):
                        raise ToriiException('Failed to update addon. Bad ZIP file: {0}.'.format(value))
                    if isinstance(addon, ToriiObject):
                        uuid = addon.uuid
                        return self._updatezip(uuid=uuid, path=value)
                    else:
                        raise ToriiException('Failed to update addon. Bad JSON addon: {0}.'.format(addon))

        return ToriiService.update(self, addon, create=False)
