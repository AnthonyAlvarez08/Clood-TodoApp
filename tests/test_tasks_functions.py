import random
import config
from data.user import User
from data.task import Task
import data.DBWrapper as DBWrapper
import auth

"""
TODO: actually write the unit tests


"""


def random_string(num_letters: int) -> str:
	alphabet = 'qwertyuiopasdfghjklzxcvbnm'
	return ''.join([random.choice(alphabet) for i in range(num_letters)])


def test_creating_task():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)

	# use this already existing user to do things
	usr = User.GetUserByEmail(dbConn, 'test@test.com')

	# create a task
	tesk = Task.Upsert(dbConn, Task("Test task", usr.userid))

	# now to retrieve it
	back = Task.GetTaskById(dbConn, tesk.taskid)

	assert back != None
	assert back.userid == usr.userid
	assert back.taskid == tesk.taskid
	assert back.title == tesk.title
	

def test_updating_task():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)

	# use this already existing user to do things
	usr = User.GetUserByEmail(dbConn, 'test@test.com')

	# create a task
	tesk = Task.Upsert(dbConn, Task("Test task 1", usr.userid))

	# now to retrieve it
	back = Task.GetTaskById(dbConn, tesk.taskid)


	assert back.title == "Test task 1"

	tesk.title = "Edited lol"

	newer = Task.Upsert(dbConn, tesk)

	assert newer != None
	assert newer.taskid == tesk.taskid
	assert newer.title == "Edited lol"




def test_deleting_task():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)

	# use this already existing user to do things
	usr = User.GetUserByEmail(dbConn, 'test@test.com')

	# create a task
	tesk = Task.Upsert(dbConn, Task("to be deleted", usr.userid))

	# delete the task
	Task.DeleteTaskByID(dbConn, tesk.taskid)

	assert Task.GetTaskById(dbConn, tesk.taskid) == None

	
	

def test_retrieving_users_tasks():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
	
	# use this already existing user to do things
	usr = User.GetUserByEmail(dbConn, 'test@test.com')

	tasklist = Task.GetOneUsersTask(dbConn, usr.userid)


	only_titles = map(lambda x: x.title, tasklist)
	only_ones_with_sample = list(filter(lambda x : x == "Test task", only_titles))

	assert len(only_ones_with_sample) > 0

	print(tasklist)