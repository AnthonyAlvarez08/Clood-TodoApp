import random
import requests
import config
import subprocess

if __name__ == '__main__':
    from ServerContext import ServerContext
else:
    from tests.ServerContext import ServerContext


URL = f'http://{config.HOST}:{config.PORT}'

VENV_EXECUTOR = r'C:\Users\antho\source\repos\TodoApp\venv\Scripts\python.exe'
APP_FILE = 'app.py'


def test_get_some_users():

    with ServerContext(VENV_EXECUTOR, APP_FILE):
    


        response = requests.get(URL + '/api/allusers')

        assert response.status_code == 200

        stuff = response.json()

        assert stuff.get('status') == 'success'
        assert len(stuff.get('users')) > 0



