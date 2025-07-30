from datetime import datetime as dt
import copy
import sys

from bson import ObjectId

from torii.data.struct import Struct, json_equals, json_diff
from torii.exception import ToriiException


class ToriiObject(Struct):
    """
    Wrapper for the torii objects
    """

    _DEEP_COPY_ORIG = True

    def __init__(self, json={}, service=None):

        if isinstance(json, ToriiObject):
            Struct.__init__(self, json.to_json())
            # always change the Id on copy
            self._id = str(ObjectId())
            self._orig = json._orig

        else:
            Struct.__init__(self, json)
            if self.__class__._DEEP_COPY_ORIG:
                self._orig = copy.deepcopy(json)
            else:
                self._orig = None

        # init the id if it was not
        if not hasattr(self, '_id'):
            self._id = str(ObjectId())

        self._service = service

    def from_json(self, json, transient_entries=None, wipe=True):
        try:
            Struct.from_json(self, json, transient_entries=transient_entries, wipe=wipe)
            if self.__class__._DEEP_COPY_ORIG:
                self._orig = copy.deepcopy(json)
            else:
                self._orig = None
        except:
            raise ToriiException('Failed convert ToriiObject \'{0}\' to Json'
                                 .format(json['name'] if 'name' in json else 'unknown')) \
                .with_traceback(sys.exc_info()[2])

    def to_json(self, ref=False, transient_entries=None):
        try:
            if ref:
                return {'id': self.id, 'name': self.name}
            else:
                json = super(ToriiObject, self).to_json(transient_entries=transient_entries)
                if 'id' in json:
                    del json['id']
                json['_id'] = self.id
                return json
        except:
            raise ToriiException('Failed convert {0} from Json'.format(self)) \
                .with_traceback(sys.exc_info()[2])

    def has_changed(self):
        return not hasattr(self, '_orig') or not json_equals(self._orig, self.to_json())

    @property
    def id(self):
        return self._id

    @property
    def diff(self):
        if not hasattr(self, '_orig'):
            return self

        diff = json_diff(self._orig, self.to_json())

        # add the id in the diff only if not empty
        if diff:
            diff['id'] = self.id

        return diff

    def clear_id(self):
        self.id = str(ObjectId())

    @property
    def orig(self):
        return self._orig

    @property
    def ref(self):
        return Struct({'id': self.id, 'name': self.name})

    def match(self, obj):
        """
        Does the object ID match another object or reference or ID string
        :param obj: the object to match
        :return: boolean
        """
        if isinstance(obj, Struct):
            return self.id == obj.id
        else:
            return self.id == obj

    def create(self):
        return self._service.create(self)

    def update(self, **kwargs):
        if (self.has_changed()):
            return self._service.update(self, **kwargs)
        else:
            return self._service.refresh(self)

    def patch(self, *args):
        return self._service.patch(self.id, *args)

    def refresh(self):
        return self._service.refresh(self)

    def action(self, action=None, params=None, update=True, send_payload=True, raw_result=True):
        return self._service.action(action=action,
                                    obj=self,
                                    params=params,
                                    update=update,
                                    send_payload=send_payload,
                                    raw_result=raw_result)

    def snapshot(self):
        return self._service.action('snapshot', self)

    def revert(self):
        return self._service.action('revert', self)
