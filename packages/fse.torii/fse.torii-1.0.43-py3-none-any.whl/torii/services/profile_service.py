from torii.exception import ToriiException
from torii.data import *
from torii.services.torii_service import ToriiService


class ProfileService(ToriiService):

    def __init__(self, torii):
        """
        Create the Profile service.

        :param torii:
        """
        ToriiService.__init__(self, torii=torii, name='profiles', object_class=ToriiObject)

    def create_profile(self, obj, task_id=''):
        """
                     Create a profile in Torii.
                     :param obj: the object to register.
                     :param taskId: task id, must be in the db.
                     :return: the modified object.
                     """

        params = {
            'taskId': task_id
        }

        try:
            if isinstance(obj, self._object_class):
                json = self.request_post(json=obj.to_json(), params=params)
                # update current object
                obj.from_json(json)
                return obj
            else:
                json = self.request_post(json=obj, params=params)
                # create a new ToriiObject
                return self._object_class(json, self)

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException(
                'Failed to create a {0} in the system\n{1}'.format(self._object_class, e)).with_traceback(
                sys.exc_info()[2])

    def update(self, obj, create=False, **kwargs):
        """
        Update an object
        :param obj:
        :return:
        """

        if create:
            try:
                self.get(obj.id)
            except:
                return self.create(obj, **kwargs)

        try:
            if isinstance(obj, self._object_class):
                if obj.has_changed() or 'taskId' in kwargs:
                    # update the remote version
                    json = self.request_post(path=obj.id, json=obj.to_json(), params=kwargs)
                else:
                    # update local version
                    json = self.request_get(path=obj.id)
            else:
                raise ToriiException('unexpected case: please think about it before removing tis exception :-)')
                json = self.request_post(path=obj['_id'], json=obj, params=kwargs)

            obj.from_json(json)

            return obj

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to update {0}\n{1}'.format(obj, e)).with_traceback(sys.exc_info()[2])

    def _prepare_params(self, params):
        prepared = {}
        if params is not None:
            for name, value in params.items():
                if value is True:
                    value = 'true'
                elif value is False:
                    value = 'false'
                prepared[name] = value
        return prepared
