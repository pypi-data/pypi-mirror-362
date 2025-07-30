import getpass

import bson
import copy
import inspect
import logging
import os
import requests
from pymongo import MongoClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

import sys

import time

from torii.managers.dao_manager import DaoManager
from torii.managers.user_manager import UserManager
from torii.services import *
from torii.data import *
from torii.exception import *
from torii.services.bs_service import BSService
from torii.session import CustomSession


def _mkdir_recursive(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        _mkdir_recursive(sub_path)
    if not os.path.exists(path):
        os.mkdir(path, 0o700)

class Torii(object):

    # the list of services proposed by the torii session
    # the value may correspond to :
    #  - a class: the service will be instanciated with the class constructor
    #  - a path: the service will be instanciated with the default service constructor using this path
    #  - nothing: the service will be instanciated with the default service constructor and default values
    __GENERIC_SERVICES = {
        'tasks': TaskService,
        'sessions': SessionService,
        'addons': AddonService,
        'applications': ApplicationService,
        'users': None,
        'bo_classes': None,
        'proxies': None,
        'scripts': None,
        'servers': None,
        'clusters': None,
        'teams': None,
        'projects': None,
        'mountpoints': None,
        'picoms': PicomService,
        'profiles': ProfileService,
        'transfers':None,
        'snapshots': None
    }

    __GENERIC_ADDON_SERVICES = {
        '98895ca2' : {'name': 'maps', 'service': 'process_mapper_98895ca2'},
        'c9a0d5e4': {'name': 'ai', 'service': AiService}
    }

    # the list of properties and their default
    __DEFAULT_PROPERTIES = {
        'base_url': 'https://localhost:8443/torii',
        'current_container': None,
        'cluster': None,
        'username': os.environ.get('USER'),
        'session_id': None,
        'private_key': os.path.expanduser('~/.ssh/id_rsa'),
        'mongo_connection_string': None,
        'use_python_dao': False,
        'use_oauth_login': False
    }

    @property
    def logger(self):
        return self._logger

    @property
    def base_url(self):
        return self.properties['base_url'] if 'base_url' in self.properties else None

    def __init__(self, properties_file=None, login=None, timeout=30,
                 username=None, password=None,
                 container=None, name=None,
                 session_id=None,
                 log_level=logging.DEBUG, save_properties=None, prompt_password=True,
                 logger=None, http_cookies=None, http_timeout=3, http_max_retries=5, db_prefix=None,
                 **kwargs):
        """

        :param properties_file:  path to the property file to use
        :param username:         username (optional)
        :param password:         password (optional)
        :param session_id        initiate the client with an existing session
        :param login:            autologin
                                 (True=force the logging, False=no logging, None=try to reuse the existing session or log in)
        :param timeout:          autologin timeout
        :param container:        use container ('new', 'current' or None)
        :param name:             name of the session
        :param log_level:        'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
        :param save_properties:  save the connection settings in the properties file
                                 (True=force the writing, False=no writing, None=only the session)
        :param http_cookies:     Cookies dict to be appended to HTTP Session
        :param http_timeout:     Default timeout for all HTTP Session requests
        :param http_max_retries: Maximum number of retries for the HTTP Session requests
        :param db_prefix:        Customer database name to filter for in bo_bases
        :param kwargs:           extra connection properties (see __DEFAULT_PROPERTIES)
        """

        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger('torii')

            # init a default handler for the logs
            self._logger.setLevel(log_level)
            ch = logging.StreamHandler()
            ch.setLevel(log_level)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)

            self._logger.addHandler(ch)

        self.init_properties(username, password, properties_file, **kwargs)

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.http_session = CustomSession()
        self.http_session.trust_env = False
        self.http_session.verify = False
        self.http_session.proxies.update({})
        self.http_session.cookies.update(http_cookies or {})

        self.session = None
        self.current_map = None
        self.current_container = None
        self.ignore_save_properties = save_properties is not None and not save_properties
        self.save_only_session_properties = save_properties is None

        # initialize database access
        self.mongo_client = MongoClient(self.properties['mongo_connection_string'])
        self.mongo_database_torii = self.mongo_client.get_database('Torii')

        self.user_manager = UserManager(self)
        self.dao_manager = DaoManager(self)

        # initialize specific services
        self.users =  ToriiService(self, 'users')
        self.proxies =  ToriiService(self, 'proxies')
        self.profiles =  ToriiService(self, 'profiles')
        self.scripts =  ToriiService(self, 'scripts')
        self.servers =  ToriiService(self, 'servers')
        self.bo_classes =  ToriiService(self, 'bo_classes')
        self.bo_bases =  ToriiService(self, 'bo_bases')
        self.clusters =  ToriiService(self, 'clusters', object_class=Cluster)
        self.teams =  ToriiService(self, 'teams')
        self.projects =  ToriiService(self, 'projects')
        self.mountpoints =  ToriiService(self, 'mountpoints')
        self.addons =  ToriiService(self, 'addons')
        self.transfers = ToriiService(self, 'transfers')
        self.organisations = OrganisationService(self)
        self.snapshots =  ToriiService(self, 'snapshots')
        self.shortcuts =  ToriiService(self, 'shortcuts')
        self.addons = ToriiService(self, 'addons')

        # initialize specific services
        self.business_services = BSService(self)
        self.files = FileService(self)
        self.graph = GraphService(self)
        self.tasks =  TaskService(self)
        self.sessions =  SessionService(self)
        self.applications =  ApplicationService(self)
        self.picoms =  PicomService(self)
        self.profiles =  ProfileService(self)
        self.addons = AddonService(self)

        # try to reuse former session
        if session_id is not None or login is None:
            self.update_session(session_id=session_id)

        # try to log automatically
        if not self.session and (login is None or login):
            self.login(prompt_password=prompt_password, timeout=timeout)
            if not self.session:
                raise ToriiException('Failed to auto-log in, please check the configuration file {0}'.format(self.property_file))

        if self.session:
            self.save_properties()

            # prepare the current container
            if container is 'current' and 'current_container' in self.properties and self.properties['current_container']:
                # reuse the former container
                self.current_container = self.tasks.get(self.properties['current_container'])
            elif container in ['new', 'current'] :
                # the user explicitely asked for a new coontainer
                self.new_container(name=name, cluster=self.properties['cluster'])
            elif container is not None:
                raise ToriiException('Unexpected container argument \'{0}\''.format(container))

            # Only update UserManager User if session exists
            if self.properties['use_python_dao']:
                self._logger.info(f"Using Direct DAO (use_python_dao={self.properties['use_python_dao']})")
                self.user_manager.update_user()


    def init_properties(self, username=None, password=None, property_file=None, **kwargs):
        """
        Init the properties from the property file
        :param property_file:
        :return:
        """
        self.properties = copy.deepcopy(self.__DEFAULT_PROPERTIES)

        # get the propety file path
        if property_file:
            self.property_file = os.path.expanduser(property_file)
        elif 'GATEWAY_PROPERTIES' in os.environ:
            self.property_file = os.environ['GATEWAY_PROPERTIES']
        elif username:
            self.property_file = os.path.expanduser('~/.torii/{}.properties'.format(username))
        else :
            self.property_file = os.path.expanduser('~/.torii/default.properties')

        # add password and username to the properties
        if username:
            self.properties['username'] = username
        if password:
            self.properties['password'] = password

        # read the property file if it exists
        if os.path.isfile(self.property_file):
            try:
                self._logger.info('Loading properties from {}'.format(self.property_file))
                properties = json.load(open(self.property_file, 'r'))

                for key, value in properties.items():
                    if key in self.__DEFAULT_PROPERTIES:
                        self.properties[key] = value
                    else:
                        self._logger.warning('Unknown property {0} = {1}'.format(key, value))

            except Exception as e:
                self._logger.warning('Failed to read the property file {0}\n{1}'.format(self.property_file, e))

        # force properties from the arguments
        for key, value in kwargs.items():
            if (key in self.__DEFAULT_PROPERTIES or key == 'password') and value is not None:
                self.properties[key] = value
            else:
                self._logger.warning('Unknown property {0} = {1}'.format(key, value))


    def get_bo_service(self, bo_name, object_class=BusinessObject):
        """
        Get a BO service.

        :param bo_name: the name of the Business Object class
        :return:
        """
        return BusinessObjectService(self, bo_name=bo_name, object_class=object_class)

    def list_bo_classes(self, explore=False):
        """
        List the BO services available

        :return:
        """
        root_bo_service = Service(self, 'bo')
        bo_class_names = root_bo_service.request_get(params={'explore':explore})

        return bo_class_names

    def save_properties(self, only_new=False):
        """
        Save the property file
        """
        try:
            # check if the property file must be overwriten at all
            if self.ignore_save_properties:
                self._logger.info('The properties wont be saved to {} (option save_properties=False)'.format(self.property_file))
                return

            # check if the property file already exists
            file_exists = os.path.isfile(self.property_file)
            if file_exists and self.save_only_session_properties:
                if self.session:
                    self.update_saved_properties('session_id', self.session.id)
                return


            self._logger.info('Saving properties to {}'.format(self.property_file))

            # prepare the properties to save
            saved_properties = dict(self.properties)
            if 'password' in saved_properties:
                del saved_properties['password']

            # create the directory if it does not exist
            _mkdir_recursive(os.path.dirname(self.property_file))
            with open(self.property_file, 'w+') as f:
                json.dump(saved_properties, f, indent=4, sort_keys=True)
                f.write('\n')

            os.chmod(self.property_file, 0o600)

        except Exception as e:
            raise ToriiException('Failed to write the property file {0}\n{1}'.format(self.property_file, e))\
                .with_traceback(sys.exc_info()[2])

    def update_saved_properties(self, key, value):

        try:
            self.properties[key] = value

            # check if the property file already exists
            file_exists = os.path.isfile(self.property_file)

            if not file_exists:
                return self.save_properties()

            self._logger.info('Updating properties to {}'.format(self.property_file))

            # read the saved property file
            with open(self.property_file, 'r') as f:
                saved_properties = json.load(f)

            # update the property file
            saved_properties[key] = value
            with open(self.property_file, 'w+') as f:
                json.dump(saved_properties, f, indent=4, sort_keys=True)
                f.write('\n')

        except Exception as e:
            raise ToriiException('Failed to update the property file {0}\n{1}'.format(self.property_file, e))\
                .with_traceback(sys.exc_info()[2])

    def update_session(self, session_id = None):
        self.session = None

        if session_id:
            # we explicitely try to udate the session so we must excet on error
            except_on_fail = True
        elif 'session_id' in self.properties:
            # in this case it is best effort
            session_id = self.properties['session_id']
            except_on_fail = False
        else:
            return None

        try:
            self.session = self.sessions.check(session_id, self.http_session.cookies)
        except Exception as e:
            if  except_on_fail:
                raise   Exception(f'Failed to reuse session {session_id}') from e
            else:
                self._logger.info(f'Failed to reuse session {session_id}, try to initiate a new session')

        if self.session:
            self.properties['session_id'] = self.session.id
            self._logger.info('Re-use session on {} as {} (created on {})'
                              .format(self.properties['base_url'],
                                      self.session.user.name,
                                      time.ctime(self.session.creationDate//1000).strip()))

        return self.session

    def login(self, username=None, password=None, prompt_password=False, retry_prompt=None, timeout=30, retry=2):
        # clear the session
        self.session = None

        login=''
        if username:
            login = username
        elif 'username' in self.properties and self.properties['username']:
            login = self.properties['username']

        secret = None

        # initialize the number of prompt retries
        if prompt_password and retry_prompt is None :
            retry_prompt = 3

        if password:
            secret = password
            comment = 'password = XXXXX'
        elif 'password' in self.properties and self.properties['password']:
            secret = self.properties['password']
            comment = 'password = XXXXX'
        elif 'private_key' in self.properties \
                and self.properties['private_key'] \
                and os.path.isfile(self.properties['private_key']):
            secret = open(self.properties['private_key'], 'r').read().rstrip('\n')
            # comment = 'private_key = {}'.format(self.properties['private_key'])
            comment = 'password = XXXXX'

        if secret is None:
            if not retry_prompt :
                self._logger.info('No more retry')
                return None
            elif not prompt_password:
                return None
            else:
                secret = getpass.getpass('Password (login={}): '.format(login))
                # comment = 'password = {}'.format(secret)
                comment = 'password = XXXXX'

        self._logger.info('Login on {} as {} ({})'
                          .format(self.properties['base_url'], login, comment))

        # initialize all the known torii services
        #for name, service in self.__GENERIC_SERVICES.items():
        #    self._expose_service(name=name, service=service)
        try:
            self.session = self.sessions.login(login, secret, timeout=timeout, oauth=self.properties['use_oauth_login'])
        except Exception as e:
            lines = str(e).splitlines()
            self._logger.error(lines[0] if lines else "Unknown error")

        if self.session:
            self.properties['session_id'] = self.session.id

            # initialize all the known torii addons services
            for addon in self.addons.list():
                if addon.installed and addon.uuid in self.__GENERIC_ADDON_SERVICES:
                    self._expose_service(**self.__GENERIC_ADDON_SERVICES[addon.uuid])

        elif prompt_password and retry_prompt is not None  and retry_prompt > 0:
            # retry to log with prompting
            self.login(username=username, retry_prompt=retry_prompt-1, prompt_password=prompt_password, timeout=timeout)
        elif retry is not None and retry > 0:
            # retry to log
            self.login(username=username, password=password, prompt_password=False, timeout=timeout, retry=retry-1)

        return self.session

    def _expose_service(self, name, service):
        """
        Expose a service as a Torii attibute
        :param name: the attribute name
        :param service: the service class or the path
        :return:
        """
        if inspect.isclass(service):
            setattr(self, name, service(self))
        else:
            setattr(self, name, ToriiService(self, name, service))

    def service(self, name, path=None):
        return ToriiService(self, name, path)


    def set_current_container(self, container=None, num=None):
        if isinstance(container, ToriiObject):
            self.current_container = container
        elif isinstance(container, str):
            self.current_container = self.tasks.get(id=container)
        elif num:
            self.current_container = self.tasks.get(num=num)
        else:
            raise ToriiException('Missing parameters')

        self.properties['current_container'] = self.current_container.id
        self.save_properties()

        return self.current_container


    def new_container(self, name=None, map=True, cluster=None):
        """
        Initiate a new container to use as current container
        TODO we should create the container independently of the
        """
        if name is None:
            name = 'Session for {0} ({1})'\
                .format(self.session.user.name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        self.current_container = self.tasks.new(type='container', name=name)


        # try to get the default cluster
        cluster_obj = None
        if isinstance(cluster, ToriiObject):
            cluster_obj = self.current_container.set_cluster(cluster)
        elif isinstance(cluster, str):
            if bson.objectid.ObjectId.is_valid(cluster):
                cluster_obj = self.clusters.get(cluster)
            else:
                cluster_obj = self.clusters.get(name=cluster)
        else:
            try:
                cluster_obj = self.clusters.get()
            except:
                pass

        if cluster_obj:
            self.current_container.set_cluster(cluster_obj)

        self.properties['current_container'] = self.current_container.id
        self.save_properties()

        return self.current_container