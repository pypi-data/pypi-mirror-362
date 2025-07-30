import bson
import os
import sys

from torii.services.service import Service
from torii.data.torii_object import ToriiObject
from torii.exception import ToriiException

class FileService(Service):

    def __init__(self, torii):
        """
        Create a generic Gateway service
        """

        Service.__init__(self, torii, "files")

    def download(self, server, path, fd, chunk_size=65536):
        """
        Download a file from the server

        :param server: the server to download from
        :param path: the absolute path on this server
        :param fd: the file descriptor to write on
        :param chunk_size: the chunk size for the streaming
        """
        if not isinstance(fd, file):
            raise ToriiException('Bad parameters, fd is mandatory')

        if not (isinstance(path, str) and path.startswith('/')):
            raise ToriiException('Bad parameters, path is mandatory and must be an absolute path (starts with /)')

        params = {'absolutePath' : path,
                  'fileName': 'default'}

        if isinstance(server, ToriiObject):
            params['serverId'] = server.id
        elif bson.objectid.ObjectId.is_valid(server):
            params['serverId'] = server
        elif isinstance(server, str):
            params['serverName'] = server
        else:
            raise ToriiException('Bad parameters, server is mandatory and must be a server object or the server name')

        try:
            r = self._torii.http_session.request(method='GET',
                                                 url=self.get_url('download'),
                                                 stream=True,
                                                 params=params)

            if r.status_code != 200:
                raise ToriiException('Failed to download {0} on {1} (code = {3})\n{2}'
                                     .format(path, server, r.reason, r.status_code))

            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks
                    fd.write(chunk)
                    fd.parse()
                    os.fsync(fd.fileno())

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to download {0} on {1} \n{2}'.format(path, server, e)).with_traceback(sys.exc_info()[2])


    def upload(self, server, path, fd):
        """
        Upload a file to the server

        :param server: the server to upload to
        :param path: the absolute path on this server (for the file or the destination directory)
        :param fd: the file descriptor to read from
        """

        if not isinstance(fd, file):
            raise ToriiException('Bad parameters, fd is mandatory')

        if not (isinstance(path, str) and path.startswith('/')):
            raise ToriiException('Bad parameters, path is mandatory and must be an absolute path (starts with /)')

        # path can contain be interpreted as a directory path or a file path
        # it depends if it ends with '/' or not
        if path.endswith('/'):
            abs_path = path[:-1]
            filename = fd.name.split('/')[-1]
        else:
            path_split = path.split('/')
            abs_path = '/'.join(path_split[0:-1]) if len(path_split) > 2 else '/{0}'.format(path_split[0])
            filename = path.split('/')[-1]

        params = {'absolutePath' : abs_path,
                  'filename': filename}

        if isinstance(server, ToriiObject):
            params['serverId'] = server.id
        elif bson.objectid.ObjectId.is_valid(server):
            params['serverId'] = server
        elif isinstance(server, str):
            params['serverName'] = server
        else:
            raise ToriiException('Bad parameters, server is mandatory and must be a server object or the server name')
        
        try:
            r = self._torii.http_session.request(method='POST',
                                                 headers={'Content-Type': 'application/octet-stream'},
                                                 url=self.get_url('direct_upload'),
                                                 params=params,
                                                 stream=True,
                                                 data=fd)
            if r.status_code not in [200, 204]:
                raise ToriiException('Failed to upload {0} from {1} (code = {2}) \n{3}'
                                     .format(path, server, r.status_code, r.reason))

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to upload {0} from {1} \n{2}'.format(path, server, e)).with_traceback(sys.exc_info()[2])

