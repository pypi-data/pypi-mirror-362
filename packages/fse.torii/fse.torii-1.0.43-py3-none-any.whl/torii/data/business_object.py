import copy
import sys

from torii.data.struct import Struct, struct_to_json
from torii.data.torii_object import ToriiObject
from torii.exception import ToriiException


class BusinessObject(ToriiObject):
    BASE_KEYS = ['_id', 'homogeneousDate', 'canEdit', 'canRemove', 'location', 'name', 'creationDate', 'modificationDate', 'description',
                 'wikiURI', 'tags', 'users', 'teams', 'projects', 'createdBy']

    def __init__(self, json={}, service=None):
        ToriiObject.__init__(self, json, service)

    @property
    def torii(self):
        return super(ToriiObject, self)

    def __getattr__(self, key):
        """
        Override 'getattr()' and dot operator
        :param key:  the attribute key
        :return:
        """

        if key == 'content':
            # we don't remove the 'content'
            return self
        else:
            return ToriiObject.__getattr__(self, key)

    def __setattr__(self, key, value):
        """
        Override 'setattr()' and dot operator
        :param key:  the attribute key
        :param value:
        :return:
        """

        if key == 'content':
            # we don't remove the 'content'
            if isinstance(value, dict):
                # legacy compatibility feature to change the wholme content of a BusinessObject
                for subkey, subvalue in value.items():
                    setattr(self, subkey, subvalue)
            else:
                raise Exception('Cannot set attribute "content"')
        else:
            ToriiObject.__setattr__(self, key, value)

    def __delattr__(self, key):
        """
        Override 'delattr()'
        :param key:  the attribute key
        :return:
        """

        if key == 'content':
            # we don't remove the 'content'
            pass
        else:
            ToriiObject.__delattr__(self, key)

    def from_json(self, json):
        try:
            ToriiObject.from_json(self, json, transient_entries=['content'])
            if 'content' in json:
                Struct.from_json(self, json['content'], transient_entries=self.__class__._TRANSIENT_ENTRIES, wipe=False)

            if self.__class__._DEEP_COPY_ORIG:
                self._orig = copy.deepcopy(json)
            else:
                self._orig = None
        except:
            raise ToriiException('Failed convert ToriiObject \'{0}\' to Json'
                                 .format(json['name'] if 'name' in json else 'unknown'))\
                .with_traceback(sys.exc_info()[2])

    def to_json(self, ref=False):
        try:
            if ref:
                return {'id': self.id, 'name': self.name}
            else:
                json = {
                    '_id':  self.id
                }
                for key in BusinessObject.BASE_KEYS:
                    if hasattr(self, key):
                        json[key] = struct_to_json(getattr(self, key))

                json['content'] = super(ToriiObject, self).to_json(transient_entries=BusinessObject.BASE_KEYS)

                if 'id' in json:
                    del json['id']

                return json
        except:
            raise ToriiException('Failed convert {0} from Json'.format(self))\
                .with_traceback(sys.exc_info()[2])


def _is_content_attr(spr, key):
    """
    Check if there the attribute must be stored in the payload
    :param key: an attribute key
    :return:
    """

    key_content_compatible = not key.startswith('_') and key != 'content'

    return key_content_compatible and not key in spr.keys()
