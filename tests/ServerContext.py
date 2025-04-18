
import subprocess
import os

# so I can work on both windows and wsl
if os.name == 'posix':
    VENV_EXECUTOR = os.getcwd() + r'/venv/bin/python3'
else:
    VENV_EXECUTOR = os.getcwd() + r'\venv\Scripts\python.exe'

APP_FILE = 'app.py'

class ServerContext:
    """
    
    Context for turning the server on and off for testing purposes

    there is probably a better way to do this but I don't care
    
    """

    def __init__(self, pypath, appfile):

        """
        Parameters
        ------------
        pypath: full path to python interpreter used for this
        appfile: name of file that runs the server
        
        
        """


        self.pypath = pypath
        self.appfile = appfile

    def __enter__(self):
        self.server = subprocess.Popen([self.pypath, self.appfile])

    def __exit__(self, exc_type='', exc_value='', exc_tb=''):
        self.server.kill()