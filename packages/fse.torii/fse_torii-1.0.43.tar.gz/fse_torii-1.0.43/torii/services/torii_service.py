from collections.abc import Iterable

__all__ = ['ToriiService']

import sys
import json as jsonlib

from torii.services.service import Service
from torii.data import ToriiObject, BusinessObject
from torii.data import Struct
from torii.exception import ToriiException


class ToriiService(Service):

    def __init__(self, torii, name, base_path=None, object_class=ToriiObject):
        """
        Create a Gateway service serving ToriiObjects
        """
        Service.__init__(self, torii, name, base_path)

        self._object_class = object_class

        self._torii = torii

    def action(self, action=None, obj=None, params=None,
               update=True,
               send_payload=True,
               raw_result=False,
               cast=None,
               service=None):
        """
        Simplified posting action
        """
        if not action or not obj:
            raise ToriiException('Missing parameters')

        # apply the action on all the elements of a sequence independently
        if not isinstance(obj, self._object_class) and isinstance(obj, Iterable):
            return [self.action(action, obji, params) for obji in obj]

        if not isinstance(obj, self._object_class):
            raise ToriiException('Wrong parameter obj, obj parameter type {0} expected'.format(self._object_class))

        if obj is not None:
            path = '{0}/{1}'.format(obj.id, action)
            # prepare the payload if the action requires the object content
            payload = obj.to_json() if send_payload else None
        else:
            path = action
            payload = None

        result = self.request('POST',
                              path=path,
                              json=payload,
                              params=params,
                              raw_result=raw_result)
        if raw_result:
            return result
        elif update:
            return obj.from_json(result)
        elif cast and issubclass(cast, ToriiObject):
            return cast(json=result, service=service if service else None)
        else:
            return Struct(json=result)

    def index(self, fields=None, default=False, unique=False):
        params = {
            'default': default,
            'unique': unique
        }

        if fields is None:
            fields = []

        return self.request_put(path='index', json=fields, params=params)

    def new(self, create=True, **kwargs):
        """
        Initialize a new shell object
        Be careful this object is not created in Gateway
        :return: the new object
        """
        try:
            params = {'create': create}
            if kwargs:
                for key, value in kwargs.items():
                    if isinstance(value, ToriiObject):
                        params[key] = value.id
                    else:
                        params[key] = value

            json = self.request_get(path='new', params=params)
            obj = self._object_class(json, self)

            return obj

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to instanciate a shell for {0}\n{1}'
                                 .format(self._object_class, e)).with_traceback(sys.exc_info()[2])

    def create(self, obj):
        """
        Register an object in torii
        :param obj: the object to register
        :return: the modified object
        """
        try:
            if isinstance(obj, self._object_class):
                json = self.request_post(json=obj.to_json())
                # update current object
                obj.from_json(json)
                obj._service = self
                return obj
            elif isinstance(obj, list):
                return self.request_post(path='bulk', json=obj)
            else:
                json = self.request_post(json=obj)
                # create a new ToriiObject
                return self._object_class(json, self)

        except ToriiException as e:
            raise e
        except Exception as e:
            raise ToriiException('Failed to create a {0} in the system\n{1}'
                                 .format(self._object_class, e)).with_traceback(sys.exc_info()[2])

    def list(self, dir='ASC', sort=None, limit=100, start=0, timeout=60, filters=None, strict_filter=False,
             include=None, no_paging=False, count=False, raw=False, cast=True, **kwargs):
        """
        List objects from the service
        :param dir: the sorting direction
        :param sort: the sorting property
        :param timeout: the request timeout in seconds
        :param limit: the maximum number of objects to be listed
        :param start: the index of the first object to be listed (regarding the sorting and filters)
        :param filters: the filters to apply
        :param strict_filter: filter the strings with 'eq' instead of 'like'
        :param include: the fields to include when getting the objects
        :param no_paging: use raw listing (no paging, no filtering)
        :param count: return the total count of elements along with the page
        :param raw: don't cast the objects in Java
        :param kwargs: quick filters

        :return: a list of objects
        """
        try:
            # mandatory if you don't want to pollute the default value and so the following calls
            # sometimes I hate python's guts !!!
            if filters is None:
                filters = []

            # add filters corresponding to the free arguments
            for key, value in kwargs.items():
                if key == 'id':
                    filters.append({'property': '_id', 'value': value, 'filterType': 'string', 'operator': 'eq'})
                elif type(value) in (float, int):
                    filters.append({'property': key, 'value': value, 'filterType': 'number', 'operator': 'eq'})
                elif isinstance(value, ToriiObject):
                    filters.append({'property': key, 'value': value.id, 'filterType': 'string', 'operator': 'eq'})
                elif strict_filter:
                    filters.append({'property': key, 'value': value, 'filterType': 'string', 'operator': 'eq'})
                else:
                    filters.append({'property': key, 'value': value, 'filterType': 'string', 'operator': 'like'})

            # request the corresponding page
            if not no_paging:
                params = {
                    'dir': dir,
                    'timeout': timeout,
                    'sort': sort,
                    'limit': limit,
                    'start': start,
                    'filter': jsonlib.dumps(filters),
                    'include': include,
                    'count': count,
                    'raw': raw
                }

                if sort:
                    params['sort'] = sort
                    params['limit'] = limit

                page = self.request_get(path='page', params=params)

                # convert the json as an object list
                if cast:
                    page_content = [self._object_class(json, self) for json in page['result']]
                else:
                    page_content = page['result']

                if count:
                    return page_content, page['size']
                else:
                    return page_content

            else:
                list = self.request_get()
                return [self._object_class(json, self) for json in list]

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to list {0}s from Gateway\n{1}'
                                 .format(self._object_class, e)).with_traceback(sys.exc_info()[2])

    def count(self, filters=None, strict_filter=False, **kwargs):
        """
        List objects from the service
        :param filters: the filters to apply
        :param strict_filter: filter the strings with 'eq' instead of 'like'
        :param kwargs: quick filters
        """

        # mandatory if you don't want to pollute the default value and so the following calls
        # sometimes I hate python's guts !!!
        if filters is None:
            filters = []

        # add filters corresponding to the free arguments
        for key, value in kwargs.items():
            if key == 'id':
                filters.append({'property': '_id', 'value': value, 'filterType': 'string', 'operator': 'eq'})
            elif type(value) in (float, int):
                filters.append({'property': key, 'value': value, 'filterType': 'number', 'operator': 'eq'})
            elif isinstance(value, ToriiObject):
                filters.append({'property': key, 'value': value.id, 'filterType': 'string', 'operator': 'eq'})
            elif strict_filter:
                filters.append({'property': key, 'value': value, 'filterType': 'string', 'operator': 'eq'})
            else:
                filters.append({'property': key, 'value': value, 'filterType': 'string', 'operator': 'like'})

        return self.request_get(path='count', params={'filter': jsonlib.dumps(filters)})

    def get(self, id=None, strict_filter=True, take_first=False, include=None, cast=True, **kwargs):
        """
        Get a single object
        :param id: the id of the object to get
        :param strict_filter: filter the strings with 'eq' instead of 'like'
        :param take_first: if several objects match the filters, take the first one
        :param kwargs: quick filters
        
        :return:
        """

        if id:
            params = {
                'include': include,
            }
            # get by id
            json = self.request_get(path=id, params=params)
            if json is not None:
                if cast:
                    return self._object_class(json, service=self)
                else:
                    return json
            else:
                return None

        else:
            # get by filter
            list = self.list(limit=10, strict_filter=strict_filter, include=include, cast=cast, **kwargs)

            if len(list) == 0:
                return None
            elif len(list) == 1 or take_first:
                return list[0]
            else:
                raise ToriiException('Several {0} match the filters (>= {1})'.format(self._object_class, len(list)))

    def refresh(self, obj):
        """
        Get the latest information from the server
        :param obj: the object to refresh
        :return:
        """
        if not isinstance(obj, self._object_class):
            raise ToriiException('Bad parameter, obj must be a {0}'.format(self._object_class.__name__))

        try:
            json = self.request_get(path=obj.id)
            obj.from_json(json)

            return obj
        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to refresh {0} in the system\n{1}'
                                 .format(self._object_class, e)).with_traceback(sys.exc_info()[2])

    def update(self, obj, create=False, cast=True, **kwargs):
        """
        Update an object
        :param obj:
        :return:
        """

        if create:
            try:
                if self.get(obj.id) is None:
                    return self.create(obj, **kwargs)
            except:
                return self.create(obj, **kwargs)

        try:
            if isinstance(obj, self._object_class):
                if obj.has_changed():
                    # update the remote version
                    json = self.request_post(path=obj.id, json=obj.to_json(), params=kwargs)
                else:
                    # update local version
                    json = self.request_get(path=obj.id)
            elif isinstance(obj, dict) and '_id' in obj:
                # update the remote version
                json = self.request_post(path=obj['_id'], json=obj, params=kwargs)
            elif isinstance(obj, list):
                obj_json = []
                for o in obj:
                    if isinstance(o, self._object_class):
                        obj_json.append(o.to_json())
                    elif isinstance(o, dict):
                        obj_json.append(o)
                    else:
                        raise ToriiException("unexpected case in list update: {}".format(type(o)))
                json = self.request_put(path='bulk', json=obj_json, params=kwargs)
                if json:
                    obj = []
                    if cast:
                        for j in json:
                            obj.append(self._object_class(j, self))
                    else:
                        obj = json
                else:
                    obj = json

                return obj
            else:
                raise ToriiException('unexpected case: please think about it before removing tis exception :-)')
                json = self.request_post(path=obj['_id'], json=obj, params=kwargs)

            if isinstance(obj, self._object_class):
                obj.from_json(json)
            else:
                obj = json

            return obj

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to update {0}\n{1}'.format(obj, e)).with_traceback(sys.exc_info()[2])

    def patch(self, id, operations):
        """
        Patch the document with given id by applying the given operations
        :param id: the id of the document
        :param operations: expected format {"op": "replace", "key": "mykey", "value": "myvalue"}
        :return:
        """
        return self.request_patch(path=id, json=operations)

    def patches(self, identified_operations=None, cast=True, **kwargs):
        """
        Patch the documents identified by applying their associated operations
        :param identified_operations: expected format {"myid": {"op": "replace", "key": "mykey", "value": "myvalue"}, }
        :param cast: cast to object or return raw json
        :return:
        """
        if identified_operations is None:
            raise ToriiException("no operation provided for patch")

        json = self.request_patch(path='', json=identified_operations, params=kwargs)
        if json:
            if cast:
                obj = [self._object_class(j, self) for j in json]
            else:
                obj = json
        else:
            obj = json
        return obj

    def delete(self, obj, force=False):
        """
        Delete an object
        :param obj: the object to refresh
        :param force: force the delete
        :return:
        """

        try:
            if isinstance(obj, self._object_class):
                self.request_delete(path=obj.id, params={"force": force})

                return obj
            elif isinstance(obj, list):
                params = {
                    'filter': jsonlib.dumps(obj),
                    'force': force
                }

                self.request_delete(path='', params=params)
            else:
                raise ToriiException('Bad parameter, obj must be a {0}'.format(self._object_class.__name__))

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to delete {0} from the system\n{1}'
                                 .format(self._object_class, e)).with_traceback(sys.exc_info()[2])

    def distinct(self, property, limit=None, filters=None, stats=None):
        """"""
        try:
            params = {}
            if limit is not None:
                params['limit'] = limit
            if filters is not None:
                params['filter'] = jsonlib.dumps(filters)
            if stats is not None:
                params['stats'] = jsonlib.dumps(stats)

            values = self.request_get(path='distinct/' + property, params=params)

            return Struct(values)
        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to get distinct values for property {0} on {1}\n{2}'
                                 .format(property, self._object_class, e)).with_traceback(sys.exc_info()[2])
