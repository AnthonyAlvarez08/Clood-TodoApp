
import subprocess


class ServerContext:
    """
    
    Context for turning the server on and off for testing purposes
    
    """

    def __init__(self, pypath, appfile):
        self.pypath = pypath
        self.appfile = appfile

    def __enter__(self):
        self.server = subprocess.Popen([self.pypath, self.appfile])

    def __exit__(self, exc_type='', exc_value='', exc_tb=''):
        self.server.kill()