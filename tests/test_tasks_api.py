import random
import requests
import config
import json

if __name__ == '__main__':
    from ServerContext import ServerContext
else:
    from tests.ServerContext import ServerContext


URL = f'http://{config.HOST}:{config.PORT}'

VENV_EXECUTOR = r'C:\Users\antho\source\repos\TodoApp\venv\Scripts\python.exe'
APP_FILE = 'app.py'

def random_string(num_letters: int) -> str:
	alphabet = 'qwertyuiopasdfghjklzxcvbnm'
	return ''.join([random.choice(alphabet) for i in range(num_letters)])



def test_creating_and_fetching_a_task():
    with ServerContext(VENV_EXECUTOR, APP_FILE):


        # create a user
        data = json.dumps({
            'email': random_string(5) + '@' + random_string(5) + '.com',
            'lastname': random_string(5),
            'firstname': random_string(5),
            'password' : random_string(5)

        })
        response = requests.post(URL + '/api/createuser', json=data)
        resdata = response.json()
        assert response.status_code == 200
        assert resdata.get('userid', 0) != 0

        userid = int(resdata['userid'])


        # give them a task
        taskdata = json.dumps({
            'title' : random_string(10)
        })
        resp2 = requests.post(URL + f'/api/newtask/{userid}', json=taskdata)
        resdata2 = resp2.json()

        # check that the task was created
        assert resp2.status_code == 200
        assert resdata2.get('taskid', 0) != 0

        # go and fetch the task
        taskid = int(resdata2['taskid'])
        resp3 = requests.get(URL + f'/api/gettasks/{userid}')

        # print(resp3, resp3.content.decode())
        resdata3 = resp3.json()

        assert resp3.status_code == 200
        assert 'tasks' in resdata3

        found = False

        for i in resdata3['tasks']:
            if str(taskid) in i:
                found = True
                break

        assert found, 'Couldnt find task in database'
        

def test_deleting_task():
    with ServerContext(VENV_EXECUTOR, APP_FILE):


        # create a user
        data = json.dumps({
            'email': random_string(5) + '@' + random_string(5) + '.com',
            'lastname': random_string(5),
            'firstname': random_string(5),
            'password' : random_string(5)

        })
        response = requests.post(URL + '/api/createuser', json=data)
        resdata = response.json()
        assert response.status_code == 200
        assert resdata.get('userid', 0) != 0

        userid = int(resdata['userid'])


        # give them a task
        taskdata = json.dumps({
            'title' : random_string(10)
        })
        resp2 = requests.post(URL + f'/api/newtask/{userid}', json=taskdata)
        resdata2 = resp2.json()

        # check that the task was created
        assert resp2.status_code == 200
        assert resdata2.get('taskid', 0) != 0
        taskid = int(resdata2['taskid'])
        

        # go on and delete the task
        resp_del = requests.delete(URL + f'/api/deletetask/{taskid}')

        assert resp_del.status_code == 200

        # go and fetch the task
        resp3 = requests.get(URL + f'/api/gettasks/{userid}')
        resdata3 = resp3.json()

        assert resp3.status_code == 200
        assert 'tasks' in resdata3

        found = False

        for i in resdata3['tasks']:
            if str(taskid) in i:
                found = True
                break

        assert not found, 'The task wasnt deleted :('