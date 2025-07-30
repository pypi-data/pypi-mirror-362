import sys

if sys.version_info >= (3, 0):
    class ToriiException(Exception):
        pass
else:
    class ToriiException(Exception):

        def with_traceback(self, x):
            return (self, None, x)
