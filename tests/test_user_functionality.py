import requests
import random
import config
from data.user import User
import data.DBWrapper as DBWrapper
import auth

"""
TODO: actually write the unit tests


"""


def random_string(num_letters: int) -> str:
	alphabet = 'qwertyuiopasdfghjklzxcvbnm'
	return ''.join([random.choice(alphabet) for i in range(num_letters)])


def test_fetching_user():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
	back = User.GetUserByEmail(dbConn, 'test@test.com')

	assert back != None
	assert back.email == 'test@test.com', f'Given back {back.email}'


def test_user_creation_internal():
	dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
	alphabet = 'qwertyuiopasdfghjklzxcvbnm'
	temp_user = User(random_string(5) + '@' + random_string(4) + '.com', auth.hash_password(random_string(15)) , 'lastanme', 'firstname')

	User.Upsert(dbConn, temp_user)

	back = User.GetUserByEmail(dbConn, temp_user.email)

	assert back != None, "Could not find user"
	assert back.email == temp_user.email, "User emails don't match"
	assert back.userid != 0, "Still has 0 as userid after fetching"



def test_user_creation_api():
	pass


def test_user_auth():
	pass




def test_user_deletetion():
	pass
