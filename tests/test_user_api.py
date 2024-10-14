import random
import requests
import config
import json
import os

if __name__ == '__main__':
    from ServerContext import ServerContext, APP_FILE, VENV_EXECUTOR
else:
    from tests.ServerContext import ServerContext, APP_FILE, VENV_EXECUTOR


URL = f'http://{config.HOST}:{config.PORT}'


def random_string(num_letters: int) -> str:
	alphabet = 'qwertyuiopasdfghjklzxcvbnm'
	return ''.join([random.choice(alphabet) for i in range(num_letters)])



def test_get_some_users():

    with ServerContext(VENV_EXECUTOR, APP_FILE):
    


        response = requests.get(URL + '/api/allusers')

        assert response.status_code == 200

        stuff = response.json()

        assert stuff.get('status') == 'success'
        assert len(stuff.get('users')) > 0


def test_create_user_success():

    with ServerContext(VENV_EXECUTOR, APP_FILE):

        data = json.dumps({
            'email': random_string(5) + '@' + random_string(5) + '.com',
            'lastname': 'haha hehe',
            'firstname': 'banana soul',
            'password' : 'new super mario bros'

        })
    
        response = requests.post(URL + '/api/createuser', json=data)
        resdata = response.json()

        print(resdata)

        assert response.status_code == 200
        assert resdata.get('status') == "success"
        assert resdata.get('userid', 0) != 0



def test_create_user_failure():

    with ServerContext(VENV_EXECUTOR, APP_FILE):


        response = requests.post(URL + '/api/createuser')
        resdata = response.json()


        assert response.status_code == 400
        assert resdata.get('error', '') != ''




