import sys
from base64 import b64encode
from json import dumps
from secrets import token_bytes

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from torii.exception import ToriiException
from torii.services.torii_service import ToriiService
from torii.data.torii_object import ToriiObject


class SessionService(ToriiService):

    def __init__(self, torii):
        """
        Create the session service
        """
        ToriiService.__init__(self, torii=torii, name='sessions', object_class=ToriiObject)


    def check_auth(self, username=None, password=None):
        credentials = SessionService._build_credentials(username, password)

        try:
            json = self.request('POST', path='login', json=credentials)
        except Exception as e:
            raise ToriiException('Failed to log as {0} on {1} : {2}'
                               .format(username, self._torii.properties['base_url'], e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)
        # self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))
        user_name = getattr(session.user, 'name', '<unknown>')
        self._logger.info('User logged as {0} on {1}'.format(user_name, self._torii.properties['base_url']))


        return session


    def login(self, username=None, password=None, timeout=30, oauth=False):
        credentials = SessionService._build_credentials(username, password)

        try:
            if oauth:
                credentials = SessionService._encrypt_credentials(credentials)
                json = self.request_post(path='microsoftApiLogin', json=credentials, timeout=timeout)
            else:
                json = self.request_post(path='login', json=credentials, timeout=timeout)
        except Exception as e:
            raise ToriiException('Failed to log as {0} on {1} : {2}'
                                 .format(username, self._torii.properties['base_url'], e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)

        self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))

        return session

    @staticmethod
    def _encrypt_credentials(creds: dict):
        cred_str = dumps(creds).encode('utf-8')
        key = AESGCM.generate_key(bit_length=256)  # Encryption Key
        iv = token_bytes(12)  # Initialization Vector
        encrypted_data = AESGCM(key).encrypt(iv, cred_str, None)  # Encrypted data

        payload = {
            'a': b64encode(encrypted_data).decode('utf-8'),
            'b': b64encode(key).decode('utf-8'),
            'c': b64encode(iv).decode('utf-8')
        }

        return payload

    def su(self, user):
        if isinstance(user, ToriiObject):
            params = {'userId': user.id}
        else:
            params = {'userId': user}

        try:
            json = self.request_post(path='su', params=params)
        except Exception as e:
            raise ToriiException('Failed to switch user with {} : {}'
                               .format(user, e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)

        self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))
        self._torii.session = session

        if self._torii.properties['use_python_dao']:
            self._torii.user_manager.update_user()

        return session


    def logout(self):
        try:
            self.request_post(path='logout')
        except Exception as e:
            raise ToriiException('Failed to logout : {}'
                               .format(self._torii.properties['base_url'], e))\
                .with_traceback(sys.exc_info()[2])

        self._logger.info('User logged out from {}'.format(self._torii.properties['base_url']))


    def check(self, session_id=None, additional_cookies={}):
        if session_id:
            params = {'ToriiSessionId': session_id}
        else:
            params = None

        try:
            url = self.get_url('check')
            http_session = requests.Session()
            http_session.trust_env = False
            http_session.verify = False
            http_session.proxies.update({})
            http_session.cookies.update({'ToriiSessionId': session_id, **{c: v for c, v in additional_cookies.items() if v}})
            response =   http_session.get(url=url, params=params)
            assert response.status_code == 200
            json = response.json()
            json = self.request_get(path='check', params=params)
        except Exception as e:
            self._logger.warn('No active session {} on {}'.format(session_id, self._torii.properties['base_url']))
            return None

        session = ToriiObject(json, self)
        self._logger.info('User {0} has an active session on {1} (id={2})'
                          .format(session.user.name, self._torii.properties['base_url'], session.id))

        return session

    @staticmethod
    def _build_credentials(username: str, password: str):
        username = username.strip()
        password = password.strip()

        return {
            'userName': username,
            'password': password
        }
