import json as json_lib
import logging
import sys

import requests
from requests_toolbelt import MultipartEncoder

from torii.exception import ToriiException


class Service(object):

    def __init__(self, torii, name, base_path=None):
        """
        Create a generic Gateway service
        """

        self.name = name
        self.base_path = base_path if base_path else name
        self._torii = torii
        self.dao_manager = torii.dao_manager
        self._logger = logging.getLogger('torii')

    def __str__(self):
        """
        Convert to string
        """
        if self.name is self.base_path:
            return 'service {0}'.format(self.name)
        else:
            return 'service {0} ({1})'.format(self.name, self.base_path)

    def get_url(self, path):
        """
        Get the Rest command URL corresponding to the relative path
        :param path: the relative path
        :return: the URL
        """
        if path.startswith('/'):
            return self._torii.properties['base_url'] + path
        else:
            return self._torii.properties['base_url'] + '/rest/' + self.base_path + '/' + path

    def get_simple_url(self, path):
        """
        Get the API path (service path + method path)

        :param path: the relative path
        :return: the API path
        """
        if path.startswith('/'):
            return path
        else:
            return self.base_path + '/' + path

    def request(self, method, path='', params=None, json=None, data=None, 
                raw_result = False, files=None, anonymous=False, timeout=None):
        """
        Submit a standard REST request
        :param method: GET, PUT, POST or DELETE
        :param path: the relative path
        :param params: the request parameters
        :param json: the Json payload
        :param data: the raw payload
        :param raw_result: return the raw result
        :param anonymous: send the request outside the HTTP session

        :return: the result as Json
        """
        try:

            headers = {}
            if data and isinstance(data, MultipartEncoder):
                headers['Content-Type'] = data.content_type

            if anonymous:
                r = requests.request(method=method,
                                     url=self.get_url(path),
                                     json=json,
                                     data=data,
                                     files=files,
                                     params=self._prepare_params(params),
                                     headers=headers,
                                     timeout=timeout)
            else:
                r = self._torii.http_session.request(method=method,
                                                     url=self.get_url(path),
                                                     json=json,
                                                     data=data,
                                                     files=files,
                                                     params=self._prepare_params(params),
                                                     headers=headers,
                                                     timeout=timeout)

            if r.status_code == 200:
                if method in ['GET', 'POST', 'PUT', 'PATCH'] and not raw_result:
                    return r.json()
                else:
                    return str(r.content)
            elif r.status_code in [204]:
                return None
            else:
                message = 'Failed to request {0} {1} on {2} (code = {3})' \
                          '\n\tserver message: \n\t\t{4}'\
                    .format(method, path, str(self), r.status_code, r.reason)\
                    .replace('\0', '')

                content = str(r.content).replace('\0', '')
                if '{' in content and '}' in content:
                    try:
                        raw_json_str = content[content.find('{'):content.rfind('}') + 1]
                        raw_json_str = raw_json_str.replace('\\n    "', '"').replace('\\n}', '}')
                        content = json_lib.loads(raw_json_str)
                        if 'message' in content:
                            message += '\n\tJava error: ' + content['message']
                        if 'detail' in content:
                            stacktrace_str = content['detail'].replace('\\n', '\n\t').replace('\\t', '\t')
                            message += '\n\tJava stacktrace: \n\t\t{0}'.format(stacktrace_str)
                    except:
                        message += '\n\t\t{0}'.format(content)
                else:
                    message += '\n\t\t{0}'.format(content)

                raise ToriiException(message)

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to request {0} {1} on {2} \n{3}'
                                 .format(method, path, str(self), e)).with_traceback(sys.exc_info()[2])

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

    def request_get(self, path='', params=None, files=None, timeout=None):
        """
        Simplified GET Rest request
        """
        try:
            service = self.dao_manager.run_service('GET', self.get_simple_url(path), params=params, files=files, timeout=timeout)
        except Exception as e:
            raise e

        return service if service is not None else self.request('GET', path=path, params=params, files=files, timeout=timeout)

    def request_post(self, path='', params=None, json=None, data=None, files=None, timeout=None):
        """
        Simplified POST Rest request
        """
        try:
            service = self.dao_manager.run_service('POST', self.get_simple_url(path), params=params, json=json, data=data, files=files, timeout=timeout)
        except Exception as e:
            raise e

        return service if service is not None else self.request('POST', path=path, params=params, json=json, data=data, files=files, timeout=timeout)

    def request_put(self, path='', params=None, json=None, data=None, files=None, timeout=None):
        """
        Simplified PUT Rest request
        """
        try:
            service = self.dao_manager.run_service('PUT', self.get_simple_url(path), params=params, json=json, data=data, files=files, timeout=timeout)
        except Exception as e:
            raise e

        return service if service is not None else self.request('PUT', path=path, params=params, json=json, data=data, files=files, timeout=timeout)

    def request_delete(self, path='', params=None, timeout=None):
        """
        Simplified DELETE Rest request
        """
        try:
            service = self.dao_manager.run_service('DELETE', self.get_simple_url(path), params=params, timeout=timeout)
        except Exception as e:
            raise e

        if service is None: self.request('DELETE', path=path, params=params, timeout=timeout)

    def request_patch(self, path='', params=None, json=None, timeout=None):
        """
        Simplified PATCH Rest request
        """
        try:
            service = self.dao_manager.run_service('PATCH', self.get_simple_url(path), params=params, json=json, timeout=timeout)
        except Exception as e:
            raise e

        return service if service is not None else self.request('PATCH', path=path, params=params, json=json, timeout=timeout)
