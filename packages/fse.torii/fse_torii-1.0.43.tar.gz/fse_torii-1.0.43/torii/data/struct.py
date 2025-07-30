import ast
import copy
import re
import sys

import numpy as np
from bson import ObjectId

from torii.exception import ToriiException


def camel2snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake2camel(name):
    components = name.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def cast_value(value):
    """
    Try to cast to float, integer, dict, bool if possible
    ast.literal_eval(node_or_string)
    Safely evaluate an expression node or a string containing a Python
    expression. The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None.

    :param value: the value to cast
    :return:
    """

    # for a simple string...
    if isinstance(value, str):
        # ast gives an best effort evaluator
        try:
            intermediate = ast.literal_eval(value)
        except:
            intermediate = value

        # ...but it is not recursive enough and it does not try to evaluate the leafs
        # it as detected so...
        if isinstance(intermediate, dict) or isinstance(intermediate, list):
            # ... if it has returned an structure, we reapply our cast_value recursively
            return cast_value(intermediate)
        else:
            # ... in case of a simple type, we stop the recursion
            return intermediate

    # for dictionaries...
    elif isinstance(value, dict):
        casted_value = {}
        for key, subvalue in value.items():

            # ... we apply the cast rescursively
            try:
                casted_subvalue = cast_value(subvalue)
            except:
                # ... and we best effort in case of pb
                casted_subvalue = subvalue

            casted_value[key] = casted_subvalue

        return casted_value

    # for the lists we use the same policy
    elif isinstance(value, list):
        casted_value = []

        for subvalue in value:
            try:
                casted_subvalue = cast_value(subvalue)
            except:
                casted_subvalue = subvalue

            casted_value.append(casted_subvalue)
        return casted_value

    # for anything else we consider there is nothing more to cast
    else:
        # ... so we end the recursion
        return value


def json_equals(old, new):
    if not isinstance(old, type(new)):
        return old == new
    elif isinstance(old, dict):
        if set(old.keys()) != set(new.keys()):
            return False

        for key, value in new.items():
            old_value = old[key]
            if not json_equals(old_value, value):
                return False
        return True
    elif isinstance(old, list):
        if len(old) != len(new):
            return False
        i = 0
        for value in new:
            old_value = old[i]
            if not json_equals(old_value, value):
                return False
            i += 1

        return True
    else:
        return old == new


def json_diff(old, new):
    diff = {}
    if not isinstance(old, type(new)):
        diff = new
    elif isinstance(old, dict):
        for key, value in new.items():
            if key not in old or not json_equals(old[key], value):
                diff[key] = value

        for key in old.keys():
            if key not in new:
                diff[key] = None

    elif isinstance(old, list):
        if not json_equals(old, new):
            diff = new

    return diff


def json_to_struct(obj):
    if isinstance(obj, dict):
        return Struct(obj)
    elif isinstance(obj, list):
        if len(obj) > 10 and not isinstance(obj[0], dict):
            return obj
        else:
            return [json_to_struct(item) for item in obj]
    elif isinstance(obj, str):
        return obj
    else:
        return copy.deepcopy(obj)


def struct_to_json(obj):
    if isinstance(obj, Struct):
        return obj.to_json(ref=True)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        if len(obj) > 10 and not isinstance(obj[0], dict) and not isinstance(obj[0], Struct):
            return obj
        else:
            return [struct_to_json(item) for item in obj]
    elif isinstance(obj, str):
        return obj
    else:
        return copy.deepcopy(obj)


class Struct(object):
    # list of entries that must remain as dictionary
    _DICT_ENTRIES = []

    # list of entries that must not appear in json
    _TRANSIENT_ENTRIES = []

    def __init__(self, json={}):
        """
        Create a proper hierarchical structure base on json-like dictionary
        """

        if json is not None:
            if '_id' in json and json['_id'] is not None:
                if isinstance(json['_id'], ObjectId):
                    json['_id'] = str(json['_id'])
                if '$oid' in json['_id']:
                    setattr(self, '_id', json['_id']['$oid'])
                else:
                    setattr(self, '_id', json['_id'])

            self.from_json(json)

    def __getattr__(self, key):
        """
        Override 'getattr()' and dot operator
        :param key:  the attribute key
        :return:
        """

        if key == 'id' and '_id' in self.__dict__:
            # we differentiate the '_id' of a ToriiObject ('_id' in json)
            # from the id that can be found in the sub documents ('id' in json)
            return self.__dict__['_id']
        elif key in self.__dict__:
            return self.__dict__[key]

        raise AttributeError

    def __setattr__(self, key, value):
        """
        Override 'setattr()' and dot operator
        :param key:  the attribute key
        :param value:
        :return:
        """
        self.__dict__[key] = value

    def __delattr__(self, key):
        """
        Override 'delattr()'
        :param key:  the attribute key
        :return:
        """
        if key in self.__dict__:
            del self.__dict__[key]

    def __iter__(self):
        """
        iterate over the attributes
        :return: an iterator
        """
        return iter(self.keys())

    def __getitem__(self, key):
        """
        Override [] operator
        :param key: the attribute key
        :return:
        """
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        """
        Override [] operator assignment
        :param key:
        :param value:
        :return:
        """
        self.__setattr__(key, value)

    def __delitem__(self, key):
        """
        Override [] operator assignment
        :param key:
        :return:
        """
        self.__delattr__(key)

    def __contains__(self, key):
        """
        Override operator 'in'
        :param key: the attribute key
        :return:
        """
        try:
            self.__getattr__(key)
        except:
            return False
        return True

    def __len__(self):
        """
        Override 'len()'
        :return:
        """
        return len(self.keys())

    def __str__(self):
        """
        String converter
        """
        if hasattr(self, 'name') and self.name:
            return '{1} {0}'.format(self.name, type(self))
        elif hasattr(self, 'num') and self.num:
            return '{1} {0}'.format(self.num, type(self))
        elif hasattr(self, 'id') and self.id:
            return '{1} {0}'.format(self.id, type(self))
        else:
            return '{0}'.format(type(self))

    def __eq__(self, other):
        """
        Override '==' operator
        :param other:
        :return:
        """
        if isinstance(other, self.__class__):
            return json_equals(self.to_json(), other.to_json())
        elif isinstance(other, dict):
            return json_equals(self.to_json(), other)
        else:
            return False

    def __ne__(self, other):
        """
        Override '!=' operator
        :param other:
        :return:
        """
        return not self.__eq__(other)

    def keys(self):
        """
        Override 'keys()'
        """

        return [key for key in self.__dict__.keys() if isinstance(key, int) or not key.startswith('_')]

    def items(self):
        """
        Override 'items()'
        """
        return [(key, self.__getattr__(key)) for key in self.keys()]

    def from_json(self, json, transient_entries=None, wipe=True):
        """
        Update the structure based on a Json compatible dictionary
        """
        key = None
        try:
            if wipe:
                # remove the former attributes
                for key in Struct.keys(self):
                    if key.startswith('_'):
                        pass
                    elif key in self.__class__._TRANSIENT_ENTRIES:
                        pass
                    elif transient_entries is not None and key in transient_entries:
                        pass
                    else:
                        self.__delattr__(key)

            # re-init them
            for key, value in json.items():
                if isinstance(key, str) and key.startswith('_'):
                    pass
                elif key in self.__class__._TRANSIENT_ENTRIES:
                    pass
                elif transient_entries is not None and key in transient_entries:
                    pass
                elif key not in self._DICT_ENTRIES:
                    Struct.__setattr__(self, key, json_to_struct(value))
                else:
                    Struct.__setattr__(self, key, value)
        except:
            raise ToriiException('Failed convert struct from Json on key \'{0}\''
                                 .format(key)).with_traceback(sys.exc_info()[2])

    def to_json(self, ref=False, transient_entries=None):
        """
        Export the structure as a Json compatible dictionary
        :param ref: export as reference (only for ToriiObject)
        """
        json = {}

        key = None
        try:
            if hasattr(self, '_id') and (not transient_entries or '_id' not in transient_entries):
                json['_id'] = self.id

            for key, value in self.items():
                if key in self._TRANSIENT_ENTRIES:
                    pass
                elif transient_entries is not None and key in transient_entries:
                    pass
                else:
                    json[key] = struct_to_json(value)

        except:
            raise ToriiException('Failed convert struct to Json on key \'{0}\''
                                 .format(key)).with_traceback(sys.exc_info()[2])

        return json
